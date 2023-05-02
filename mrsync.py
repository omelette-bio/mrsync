#! /usr/bin/env python3

"""
program to synchronize files between two directories localy, using pipes
"""

import options, sender, message, generator, server
import sys, os, signal

# parse the arhuments
args = options.parsing()



# if -h or --help is used, print the help and exit
if args.help:
   options.help()
   sys.exit(0)



# if --list-only is used, list the files and exit
if args.list_only:
   file_dict, dirs = sender.list_files(args.source, args)
   options.listing(generator.sort_by_path(file_dict))
   sys.exit(0)


# defines the handler for the signals
def handler(signum, frame):
   global pipes, pipe_state
   print(f"Interrupted {os.getpid()}, exiting...", file=sys.stderr)
   for fd in pipes:
      os.close(fd)
   pipe_state = "off"

signal.signal(signal.SIGINT, handler)
signal.signal(signal.SIGUSR1, handler)



# connect to server with pipe
# fork to create a child process which will be the server

fdr1, fdw1 = os.pipe()
fdr2, fdw2 = os.pipe()



pid_server = os.fork()
#server process, read on fdr1, write on fdw2
if pid_server == 0:
   
   # store the state of the pipe
   pipe_state = "on"
   
   # close unused pipes
   os.close(fdw1)
   os.close(fdr2)
   
   # create the list of pipes the server uses
   pipes = [fdr1, fdw2]
   
   
   # when starting, send the pid to the client
   message.send(fdw2, "pid", os.getpid())
   pid_client = message.receive(fdr1)[1]
   
   
   if args.verbose > 1:
      print("Client pid: ", pid_client, file=sys.stderr)
   
   
   
   # create the list of files at the destination
   os.chdir(args.destination)
   
   # we try to create the list of files at the destination
   try:
      destination_files = sender.list_files(".", args)
   # if it fails, we send a signal to the client and exit
   except:
      print("Error while creating server file list", file=sys.stderr)
      os.kill(pid_client, signal.SIGUSR1)
      os.close(fdr1)
      os.close(fdw2)
      sys.exit(3)
   
   # we sort the list of files
   destination_files = generator.sort_by_path(destination_files)
   
   
   # receive the list of files to send
   (tag,v) = message.receive(fdr1)


   # we sort the list of files to send
   files_to_send = generator.sort_by_path(v)

   
   # generator to send files
   if os.fork() == 0:
      
      # create the list of files to send, modify and delete
      send, modify, delete = generator.compare(files_to_send, destination_files, args)
      
      state = "send"
      # we send the lists to the client, if it's not empty
      if len(send) > 0:
         message.send(fdw2, "send", send)

      if len(modify) > 0:
         message.send(fdw2, "modify", modify)
      
      if len(delete) > 0:
         message.send(fdw2, "delete", delete)
      
      # if nothing has to be sent, modified or deleted, we send "end"
      if len(send) == 0 and len(modify) == 0 and len(delete) == 0:
         message.send(fdw2, "end", "No files to send/modify/delete")
         state = "end"
      
      if state == "send":
         message.send(fdw2, "end", "No more to send/modify/delete")
         state = "end"
      
      # and then, we close the pipes and exit
      os.close(fdw2)
      os.close(fdr1)
      sys.exit(0)
   
   
   os.wait()
   
   # now receive the files to copy and the files to modify
   while pipe_state == "on":
      
      # receive the message
      (tag,v) = message.receive(fdr1)
      
      # if there is a problem in the files received, we send a signal to the client and exit
      if tag == "received-nothing":
         print("Error in files received, exiting...", file=sys.stderr)
         os.kill(pid_client, signal.SIGUSR1)
         os.close(fdw2)
         os.close(fdr1)
         sys.exit(11)
      
      
      # if the message is a tuple, that means we got a file to copy
      if type(v) == tuple:
         
         #we split the tuple 
         file, folder, data, modif, perms = v
         
         # if the tag is "sendfile", we create the file and write the data in it
         if tag == "sendfile":
            
            #check if the folder exists, if not create it
            if folder != "":
               if not os.path.isdir(folder):
                  os.makedirs(folder)
                  if args.verbose > 0:
                     print(f"Creating folder {folder}", file=sys.stderr)
            
            #create the file
            file = os.path.join(folder, os.path.basename(file))
            currentfile = os.open(file, os.O_CREAT | os.O_WRONLY)
         
            
            if args.verbose > 0:
               print(f"Receiving {file}...", file=sys.stderr)
            
            # if the user wants to copy perms and times, we do it
            if args.perms or args.archive:
               if args.verbose > 0:
                  print(f"Changing permissions of {file} to {perms}", file=sys.stderr)
               os.chmod(file, perms)
            
            #change the standard output to the file
            os.dup2(currentfile, 1)
            
            
            #write the data
            os.write(1, data)
            os.close(currentfile)

            # if the user wants to copy times, we do it
            if args.times or args.archive:
               if args.verbose > 0:
                  print(f"Changing times of {file} to {modif}", file=sys.stderr)
               os.utime(file, (modif, modif))



         if tag == "modifyfile":
            
            #check if the folder exists, if not create it
            if folder != "":
               if not os.path.isdir(folder):
                  os.makedirs(folder)
                  if args.verbose > 0:
                     print(f"Creating folder {folder}", file=sys.stderr)
            
            #create the file
            file = os.path.join(folder, os.path.basename(file))
            currentfile = os.open(file, os.O_CREAT | os.O_WRONLY)
            
            
            
            if args.verbose > 0:
               print(f"Receiving {file}...", file=sys.stderr)
            
            # if the user wants to copy perms, we do it
            if args.perms or args.archive:
               if args.verbose > 0:
                  print(f"Changing permissions of {file} to {perms}", file=sys.stderr)
               os.chmod(file, perms)
            
            #change the standard output to the file
            os.dup2(currentfile, 1)
            
            #write the data
            os.write(1, data)
            os.close(currentfile)
            
            # if the user wants to copy times, we do it
            if args.times or args.archive:
               if args.verbose > 0:
                  print(f"Changing times of {file} to {modif}", file=sys.stderr)
               os.utime(file, (modif, modif))
      
      # if the message is fully received, we display a message
      elif tag == "endfile" and args.verbose > 0:
         print(f"Done", file=sys.stderr)
         print("")
      
      # if the message is "end", we exit and change the standard output to the terminal 
      elif tag == "end":
         os.dup2(1, 1)
         break
   
   # close the pipes
   if pipe_state == "on":
      os.close(fdw2)
      os.close(fdr1)
      sys.exit(0)
   else:
      sys.exit(20)


pid_client = os.fork()

#client process, read on fdr2, write on fdw1
if pid_client == 0:
   
   pipe_state = "on"
   # close the unnecessary pipes
   os.close(fdw2)
   os.close(fdr1)
   # then store the pipes in a list, to close it with a loop
   pipes = [fdr2, fdw1]
   
   # get the pid of the server, then send our pid to the server
   pid_server = message.receive(fdr2)[1]
   message.send(fdw1, "pid", os.getpid())
   
   if args.verbose > 1:
      print(f"Server pid : {pid_server}")
   
   
   # create the list of files at the source
   try:
      files = sender.list_files(args.source, args)
   # if there is an error, we exit
   except:
      print("Error while creating Client's file list, exiting...", file=sys.stderr)
      os.kill(pid_server, signal.SIGUSR1)
      os.close(fdr2)
      os.close(fdw1)
      sys.exit(3)
      
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
         
      # if the message is a list of files to send, we store it
      if tag == "send":
         send_list = v
      
      # if the message is a list of files to modify, we store it
      elif tag == "modify":
         modify_list = v

      # if the message is a list of files to delete, we delete them
      elif tag == "delete" and args.delete:
         server.order_list_delete(v)
         for file in v:
            os.remove(os.path.join(args.destination, file))
            # if the folder is empty, delete it
            if os.path.dirname(file) != "":
               if not os.listdir(os.path.join(args.destination,os.path.dirname(file))):
                  os.rmdir(os.path.join(args.destination,os.path.dirname(file)))
   
   # now for each file to send, we send the name, his path and the content
   if send_list != []:
      
      for file in send_list:
         
         # we verify each time if the pipe is still open, if not it means the server has crashed or exited
         if pipe_state == "on":
            
            # if there are multiple sources, we remove the first folder of the path
            if len(args.source) > 1:
               file = '/'.join(file.split('/')[1:])
            
            # we get the full path of the file
            full_path = os.path.join(files[file][0], file)
            
            if args.verbose > 0:
               print(f"Sending : {full_path}")
            
            # and then we try to open it
            try:
               sending_file = os.open(full_path, os.O_RDONLY)
            # if it's impossible, we exit
            except:
               print(f"Error while opening {file}", file=sys.stderr)
               os.kill(pid_server, signal.SIGUSR1)
               os.close(fdw1)
               os.close(fdr2)
               sys.exit(11)
            
            if args.verbose > 0:
               print(f"Reading...")
               print("")
            
            
            # if we opened the file successfully, read the file and send it, in multiple parts if size > 16 Mo
            while True:
               
               # we try to read the file
               try:
                  data = os.read(sending_file, 16*1024*1024)
               # if it's impossible, we exit
               except:
                  print(f"Error while reading {file}", file=sys.stderr)
                  os.kill(pid_server, signal.SIGUSR1)
                  os.close(sending_file)
                  os.close(fdw1)
                  os.close(fdr2)
                  sys.exit(11)
               
               # we calculate the folder of the file
               folder = ""
               
               if len(args.source) > 1 and sender.all_path_dir(args.source):
                  if os.path.dirname(file) == "":
                     folder = os.path.basename(files[file][0])
                  
                  else:
                     folder = os.path.join(os.path.basename(files[file][0]), os.path.dirname(file))
               
               else:
                  if os.path.dirname(file) != "":
                     folder = os.path.dirname(file)
               
               # and then we send the file, with the name, the folder, the content, the size, the last modification date and permissions
               message.send(fdw1, "sendfile", (file, folder, data, files[file][2], files[file][3]))
               
               # send "endfile" if there the file has been read entirely
               if len(data) < 16*1024*1024:
                  message.send(fdw1, "endfile", "endfile")
                  break
            
            # and then we close the file
            os.close(sending_file)
   
   # the modifying system is the same as the sending system, because it's in case we create the way to send only the modifications
   if modify_list != []:
      
      # iterate over the list of files to modify
      for file in modify_list:
         
         # we verify each time if the pipe is still open, if not it means the server has crashed or exited
         if pipe_state == "on":
            
            # if there are multiple sources, we remove the first folder of the path
            if len(args.source) > 1:
               file = '/'.join(file.split('/')[1:])
            
            # we get the full path of the file
            full_path = os.path.join(files[file][0], file)
            
            if args.verbose > 0:
               print(f"Sending : {full_path}")
               
            # and then we try to open it
            try:
               sending_file = os.open(full_path, os.O_RDONLY)
            # if it's impossible, we exit
            except:
               print(f"Error while opening {file}", file=sys.stderr)
               os.kill(pid_server, signal.SIGUSR1)
               os.close(fdw1)
               os.close(fdr2)
               sys.exit(11)
            
            if args.verbose > 0:
               print(f"Reading...")
               print("")
               
            # read the file and send it, in multiple parts if size > 16 Mo
            while True:
               
               # we try to read the file
               try:
                  data = os.read(sending_file, 16*1024*1024)
               # if it's impossible, we exit
               except:
                  print(f"Error while reading {file}", file=sys.stderr)
                  os.kill(pid_server, signal.SIGUSR1)
                  os.close(sending_file)
                  os.close(fdw1)
                  os.close(fdr2)
                  sys.exit(11)

               # we calculate the folder of the file
               folder = ""
               
               if len(args.source) > 1:
                  if os.path.dirname(file) == "":
                     folder = os.path.basename(files[file][0])
                  
                  else:
                     folder = os.path.join(os.path.basename(files[file][0]), os.path.dirname(file))
               
               else:
                  if os.path.dirname(file) != "":
                     folder = os.path.dirname(file)
               
               # then we send the file, with the name, the folder, the content, the size, the last modification date and permissions
               message.send(fdw1, "modifyfile", (file, folder, data, files[file][2], files[file][3]))
               
               # send "endfile" if there the file has been read entirely
               if len(data) < 16*1024*1024:
                  message.send(fdw1, "endfile", "endfile")
                  break
            
            # and then we close the file
            os.close(sending_file)   
   
  
   
   # if there are no files to send, we send "end" to the server
   if modify_list == [] and send_list == []:
      message.send(fdw1, "end", "end")
   
   # when we have sent all the files, we send "end" to the server
   message.send(fdw1, "end", "end")
   
   # finally we close the pipes, and exit
   if pipe_state == "on":
      os.close(fdw1)
      os.close(fdr2)
      sys.exit(0)
   
   # if the pipe is closed, it means the server has crashed or exited
   else:
      sys.exit(20)

# take the exit code of the server and client, and return the right exit code
status = os.waitpid(pid_server, 0)[1]
status2 = os.waitpid(pid_client, 0)[1]
# return the highest exit code
sys.exit(max(status, status2))