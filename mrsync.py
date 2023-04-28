import options, sender, message, generator, server
import sys, os

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
   
   # now receive the files to copy and the files to modify
   
   while True:
      (tag,v) = message.receive(fdr1)
      if type(v) == tuple:
         file, folder, data = v
         print(f"Receiving {file}...")
      
         if tag == "sendfile":
            #check if the folder exists, if not create it
            if not os.path.isdir(folder):
               os.makedirs(folder)
               if args.verbose > 0:
                  print(f"Creating folder {folder}")
            
            #create the file
            file = os.path.join(folder, os.path.basename(file))
            currentfile = os.open(file, os.O_CREAT | os.O_WRONLY)
            
            #change the standard output to the file
            
            os.dup2(currentfile, 1)
            
            #write the data
            os.write(1, data)
            os.close(currentfile)

      elif tag == "end":
         os.dup2(1, 1)
         break
      
   
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
   send_list = []
   modify_list = []
   
   while tag != "end":
      
      (tag, v) = message.receive(fdr2)
      
      if args.verbose > 0:
         print(f"{tag} : {v}")
         print("")
      if tag == "send":
         send_list = v
      elif tag == "modify":
         modify_list = v
   
   # now for each file to send, we send the name, his path and the content
   if send_list != []:
      
      for file in send_list:
         
         full_path = os.path.join(files[file][0], file)
         
         if args.verbose > 0:
            print(f"Sending : {full_path}")
         
         sending_file = os.open(full_path, os.O_RDONLY)
         
         if args.verbose > 0:
            print(f"Reading : {full_path}")
            print("")
            
         # read the file and send it, in multiple parts if size > 16 Mo
         while True:
            data = os.read(sending_file, 16*1024*1024)
            
            if not data:
               message.send(fdw1, "endfile", "end")
               break
            
            if os.path.dirname(file) == "":
               folder = os.path.basename(files[file][0])
            
            else:
               folder = os.path.join(os.path.basename(files[file][0]), os.path.dirname(file))
            
            message.send(fdw1, "sendfile", (file, folder, data))
         
         os.close(sending_file)
      
      message.send(fdw1, "end", "end")
      
   
   
   
   os.close(fdw1)
   os.close(fdr2)
   sys.exit(0)

sys.exit(0)