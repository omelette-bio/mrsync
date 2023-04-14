import os, argparse

def all_truc_dir(path):
   all = True
   for i in path:
      if not os.path.isdir(i):
         all = False
   return all

# path is a list of paths and files to list, if recursive is true, list all files in subdirectories
def list_files(path, recursive=False):
   files = []
   directories = []
   for i in path:
      if i[0] == "." or i[0] == "_" or i[0] == "~":
         pass
      elif not os.path.isdir(i):
         files.append(i)
      else:
         directories.append(i)
   
   if all_truc_dir(path):
      directories = path
         
   if all_truc_dir(path) and not recursive:
      for j in os.listdir(directories[0]):
         if j[0] == "." or j[0] == "_" or j[0] == "~":
            pass
         elif os.path.isdir(j):
            pass
         else:
            files.append(j)
   
   if recursive:
      while len(directories) > 0:
         for j in os.listdir(directories[0]):
            if j[0] == "." or j[0] == "_" or j[0] == "~":
               pass
            elif os.path.isdir(j):
               directories.append(os.path.join(directories[0]) + "/" + j)
            else:
               files.append(os.path.join(directories[0]) + "/" + j)
         directories.pop(0)
      
   return files

if __name__ == "__main__":
   parser = argparse.ArgumentParser()
   parser.add_argument("path", help="path to list files from")
   args = parser.parse_args()
   
   
   print(list_files(args.path, True))
   print(list_files(args.path))