import options, sys, sender, os, message, generator

args = options.parsing()

if args.list_only: 
   options.listing(args.source)
   sys.exit(0)

# connect to server with pipe
# fork to create a child process which will be the server

fdr1, fdw1 = os.pipe()
fdr2, fdw2 = os.pipe()

#server process, read on fdr1, write on fdw2
if os.fork() == 0:
   # close unused pipes
   os.close(fdw1)
   os.close(fdr2)
   # create the list of files at the destination
   os.chdir(args.destination)
   destination_files = sender.list_files(".", args)
   # receive the list of files to send
   (tag,v) = message.receive(fdr1)
   # generator to send files
   if os.fork() == 0:
      list_to_send, list_to_modify, list_to_delete = generator.compare(v, destination_files)
      print("list_to_send", list_to_send)
      print("list_to_modify", list_to_modify)
      print("list_to_delete", list_to_delete)
      sys.exit(0)
   os.close(fdw2)
   os.close(fdr1)
   sys.exit(0)


#client process, read on fdr2, write on fdw1
if os.fork() == 0:
   os.close(fdw2)
   os.close(fdr1)
   files = sender.list_files(args.source, args)
   message.send(fdw1, "files to send", files)
   # wait for request messages
   os.close(fdw1)
   os.close(fdr2)
   sys.exit(0)

sys.exit(0)