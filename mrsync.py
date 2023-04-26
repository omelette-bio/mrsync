import options, sys, sender, os, message, generator

args = options.parsing()

if args.list_only: 
   options.listing(generator.sort_by_path(sender.list_files(args.source, args)))
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
   destination_files = generator.sort_by_path(sender.list_files(".", args))
   
   # receive the list of files to send
   (tag,v) = message.receive(fdr1)
   
   files_to_send = generator.sort_by_path(v)
   # generator to send files
   if os.fork() == 0:
      # create the list of files to send, modify and delete
      send, modify, delete = generator.compare(files_to_send, destination_files)

      state = "send"
      # we send some requests to the client, if it's not empty
      if len(send) > 0:
         message.send(fdw2, "send", send)

      if len(modify) > 0:
         message.send(fdw2, "modify", modify)
      
      if len(send) == 0 and len(modify) == 0:
         message.send(fdw2, "end", "No files to send or modify")
         state = "end"
      
      if state == "send":
         message.send(fdw2, "end", "No more to send/modify")
      
      
      os.close(fdw2)
      sys.exit(0)
   
   os.wait()
   
   os.close(fdw2)
   os.close(fdr1)
   sys.exit(0)


#client process, read on fdr2, write on fdw1
if os.fork() == 0:
   # close the unnecessary pipes
   os.close(fdw2)
   os.close(fdr1)
   
   # create the list of files at the source
   files = sender.list_files(args.source, args)
   # and send it to the server
   message.send(fdw1, "data", files)
   
   # wait for request messages from the generator
   tag = ""
   while tag != "end":
      (tag, v) = message.receive(fdr2)
      if args.verbose > 0:
         print(f"{tag} : {v}")
   
   os.close(fdw1)
   os.close(fdr2)
   sys.exit(0)

sys.exit(0)