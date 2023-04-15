import options, sys, sender, os

args = options.parsing()
files_to_send = sender.list_files(args.source, args)

if args.list_only: sys.exit(0)

# connect to server with pipe
# fork to create a child process which will be the server

fdr1, fdw1 = os.pipe()
fdr2, fdw2 = os.pipe()

#server process
if os.fork() == 0:
   os.close(fdw1)
   os.close(fdr2)
   destination_files = sender.list_files(args.destination, args)
   print(files_to_send)
   print(destination_files)


#client process
if os.fork() == 0:
   os.close(fdw2)
   os.close(fdr1)

sys.exit(0)