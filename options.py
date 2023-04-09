import argparse, os, sys


parser = argparse.ArgumentParser()

# required arguments for source and destination
parser.add_argument("source", help="source file or directory")
parser.add_argument("destination", help="destination file or directory")


# options to display or hide program output
# verbose is a counter, so -v is verbose, -vv is more verbose, etc.
# and quiet is a boolean, so -q is quiet
# we can't have -v and -q at the same time
parser.add_argument("-v", "--verbose", action="count", default=0, help="increase output verbosity")
parser.add_argument("-q", "--quiet", action="store_true", help="suppress non-error messages")


parser.add_argument("-a", "--archive", help="archive mode", action="store_true")
parser.add_argument("-r", "--recursive", help="recurse into directories", action="store_true")
parser.add_argument("-u", "--update", help="skip files that are newer on the receiver", action="store_true")
parser.add_argument("-d", "--dirs", help="transfer directories without recursing", action="store_true")
parser.add_argument("-H", "--hard-links", help="preserve hard links", action="store_true")
parser.add_argument("-p", "--perms", help="preserve permissions", action="store_true")
parser.add_argument("-t", "--times", help="preserve times", action="store_true")
parser.add_argument("--existing", help="skip creating new files on receiver", action="store_true")
parser.add_argument("--ignore-existing", help="skip updating files that exist on receiver", action="store_true")
parser.add_argument("--delete", help="delete extraneous files from dest dirs", action="store_true")
parser.add_argument("--force", help="force deletion of dirs even if not empty", action="store_true")
parser.add_argument("--timeout", help="set I/O timeout in seconds", type=int)
parser.add_argument("--blocking-io", help="use blocking I/O for the remote shell", action="store_true")
parser.add_argument("-I", "--ignore-times", help="don't skip files that match in size and time", action="store_true")
parser.add_argument("--size-only", help="skip files that match in size", action="store_true")
parser.add_argument("--list-only", help="list the files instead of copying them", action="store_true")


#commands to run with daemon, this help shows only when --daemon is used
parser.add_argument("--daemon", help="run as an mrsync daemon", action="store_true")
parser.add_argument("--address", help="bind to the specified address", type=str)
parser.add_argument("--no-detach", help="do not detach from the parent", action="store_true")
parser.add_argument("--port", help="listen on alternate port number", type=str)



# function to call to parse the arguments
# if -v and -q are used together, print an error and exit
def parsing():
   args = parser.parse_args()
   if ((args.verbose > 0) and (args.quiet)):
      print("\033[91mError: -v and -q cannot be used together\033[0m")
      sys.exit(1)
   return args


# function to call to list the contents of a directory
# useful later for listing files to send
def listing(directory):
   if os.fork() == 0: 
      os.execvp("ls", ["ls", "-l", directory])
   else:
      os.wait()





# verify that it works
if __name__ == "__main__":
   args = parsing()
   for arg in vars(args):
      print("{} : \t{}".format(arg, getattr(args, arg)))