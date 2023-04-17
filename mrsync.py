import options, sys, sender, os, message, time

args = options.parsing()

if args.list_only: 
   sender.list_files(args.source, args)
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
   destination_files = sender.list_files(args.destination, args)
   # receive the list of files to send
   (tag,v) = message.receive(fdr1)
   print("received",tag,v)
   


#client process, read on fdr2, write on fdw1
if os.fork() == 0:
   os.close(fdw2)
   os.close(fdr1)
   files = sender.list_files(args.source, args)
   message.send(fdw1, "files to send", files)

sys.exit(0)