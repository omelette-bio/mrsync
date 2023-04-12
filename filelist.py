import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to list files from")
args = parser.parse_args()


def list_files(path, mode="normal"):
   os.chdir(path)
   print(os.getcwd())
   directories = [path]
   files = []

   # List all files and if there is a directory list the files inside it
   while len(directories) > 0:
      for i in os.listdir(os.getcwd()):
         if i[0] == "." or i[0] == "_" or i[0] == "~":
            pass
         elif os.path.isdir(i) and mode == "recursive":
            directories.append(os.path.join(os.getcwd()) + "/" + i)
         else:
            files.append(i)
      if mode == "recursive":
         os.chdir(directories.pop())
      else:
         directories.pop()
   return(files)

"""
def list_files(path):
   os.chdir(path)
   print(os.getcwd())
   files = []

   for i in os.listdir(os.getcwd()):
      if os.path.isfile(i):
         files.append(i)

   return(files)
"""

print(list_files(args.path, "recursive"))
print(list_files(args.path))