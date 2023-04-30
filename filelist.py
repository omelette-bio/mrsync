import os, argparse

def all_obj_dir(path):
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
      # if the file is a symbolic link, we skip it and display message "skipping non-regular file"
      elif os.path.islink(i):
         print("skipping non-regular file")
         pass
      elif not os.path.isdir(i):
         files[i] = [os.getcwd(), os.stat(i).st_size, os.stat(i).st_mtime, os.stat(i).st_mode]
      else:
         if i[0] == "/":
            directories.append(i)
         else:
            directories.append(os.getcwd()+i)
   
   if all_obj_dir(path):
      if type(path) == str:
         directories.append(path)
      else:
         directories = path.copy()
   
   if all_obj_dir(path) and not recursive:
      for i in directories:
         os.chdir(i)
         for j in os.listdir(i):
            if j[0] == "." or j[0] == "_" or j[0] == "~":
               pass
            elif os.path.isdir(j):
               pass
            # if the file is a symbolic link, we skip it and display message "skipping non-regular file"
            elif os.path.islink(j):
               print("skipping non-regular file")
               pass
            else:
               files[j] = [os.getcwd(), os.stat(j).st_size, os.stat(j).st_mtime, os.stat(j).st_mode]
   
   base_directories = []
   
   if recursive:
      files_list = []
      while len(directories) > 0:
         os.chdir(directories[0])
         directory = os.getcwd()
         if directories[0] in path:
            base_directories.append(directory)
         for j in os.listdir(directory):
            # add the parent directory to the file name and remove the parent folder from the path if we are in a subdirectory
            if j[0] == "." or j[0] == "_" or j[0] == "~":
               pass
            # if the file is a symbolic link, we skip it and display message "skipping non-regular file"
            elif os.path.islink(j):
               print("skipping non-regular file")
               pass
            elif os.path.isdir(j):
               if directory[-1] == "/":
                  directories.append(os.path.join(directory) + j)
               else:
                  directories.append(os.path.join(directory) + "/" + j)
            else:
               # while we are in a subdirectory, add the parent directory to the file name
               directory_backup = directory
               while directory not in base_directories:
                  j = os.path.basename(directory) + "/" + j
                  directory = os.path.dirname(directory)
               files_list.append(j)
               directory = directory_backup
         directories.pop(0)
      
      # for each file in files_list, add it to the files dictionnary, with the path, size and last modification time
      for i in base_directories:
         os.chdir(i)
         for j in files_list:
            if os.path.exists(os.path.join(i, j)):
               files[j] = [i, os.stat(j).st_size, os.stat(j).st_mtime, os.stat(j).st_mode]
         
         
   return files

if __name__ == "__main__":
   parser = argparse.ArgumentParser(description="List files in a directory")
   parser.add_argument("path", nargs="+", help="Path to list")
   parser.add_argument("-r", "--recursive", action="store_true", help="List files in subdirectories")
   args = parser.parse_args()
   liste = list_files(args.path, args.recursive)
   for i in liste:
      print(i, liste[i])
   