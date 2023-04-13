import os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("path", help="path to list files from")
args = parser.parse_args()


def list_files(path, recursive=False):
   os.chdir(path)
   print(os.getcwd())
   directories = [path]
   files = []

   while len(directories) > 0:
      for i in os.listdir(os.getcwd()):
         if i[0] == "." or i[0] == "_" or i[0] == "~":
            pass
         elif os.path.isdir(i) and recursive:
            directories.append(os.path.join(os.getcwd()) + "/" + i)
         else:
            files.append(i)
      if recursive:
         os.chdir(directories.pop())
      else:
         directories.pop()
   return(files)

if __name__ == "__main__":
   print(list_files(args.path, True))
   print(list_files(args.path))