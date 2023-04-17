import os, argparse, generator

def all_truc_dir(path):
   all = True
   for i in path:
      if not os.path.isdir(i):
         all = False
   return all

# path is a list of paths and files to list, if recursive is true, list all files in subdirectories
def list_files(path, recursive=False):
   files = {}
   directories = []
   for i in path:
      if i[0] == "." or i[0] == "_" or i[0] == "~":
         pass
      elif not os.path.isdir(i):
         files[i] = [os.getcwd(), os.stat(i).st_size, os.stat(i).st_mtime]
      else:
         if i[0] == "/":
            directories.append(i)
         else:
            directories.append(os.getcwd()+i)
   
   if all_truc_dir(path):
      if type(path) == str:
         directories.append(path)
      else:
         directories = path
   
   if all_truc_dir(path) and not recursive:
      for j in os.listdir(directories[0]):
         if j[0] == "." or j[0] == "_" or j[0] == "~":
            pass
         elif os.path.isdir(j):
            pass
         else:
            files[j] = [os.getcwd(), os.stat(j).st_size, os.stat(j).st_mtime]
   
   if recursive:
      while len(directories) > 0:
         os.chdir(directories[0])
         directory = os.getcwd()
         for j in os.listdir(directory):
            if j[0] == "." or j[0] == "_" or j[0] == "~":
               pass
            elif os.path.isdir(j):
               if directory[-1] == "/":
                  directories.append(os.path.join(directory) + j)
               else:
                  directories.append(os.path.join(directory) + "/" + j)
            else:
               files[j] = [os.getcwd(), os.stat(j).st_size, os.stat(j).st_mtime]
         directories.pop(0)
      
   return files

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description="List files in a directory")
   parser.add_argument("path", nargs="+", help="Path to list")
   parser.add_argument("-r", "--recursive", action="store_true", help="List files in subdirectories")
   args = parser.parse_args()
   liste = list_files(args.path, args.recursive)
   for i in liste:
      print(i, liste[i])
   