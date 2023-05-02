import os, argparse

# for each file in path, if it is a directory, return True, else return False
def all_obj_dir(path):
   all = True
   for i in path:
      if not os.path.isdir(i):
         all = False
   return all

# path is a list of paths and files to list, if recursive is true, list all files in subdirectories
def list_files(path, args, recursive=False):
   files = {}
   directories = []
   
   for i in path:
      # if the file is a hidden file, we skip it
      if i[0] == "." or i[0] == "_" or i[0] == "~":
         pass
      
      # if the file is a symbolic link, we skip it and display message "skipping non-regular file"
      elif os.path.islink(i) and not args.quiet:
         print("skipping non-regular file")
         pass
      
      # if the file is a regular file, we put it in the dictionnary
      elif not os.path.isdir(i):
         # put the full path of the file in the dictionnary
         if os.path.dirname(i) == "":
            files[os.path.basename(i)] = [os.getcwd(), os.stat(i).st_size, os.stat(i).st_mtime, os.stat(i).st_mode]
         else:
            files[os.path.basename(i)] = [os.path.dirname(i), os.stat(i).st_size, os.stat(i).st_mtime, os.stat(i).st_mode]
      
      # if the file is a directory, we put it in the list of directories
      else:
         if i[0] == "/":
            directories.append(i)
         else:
            directories.append(os.getcwd()+i)
   
   # now if all the elements in path are directories, we list all the files in the directories list
   if all_obj_dir(path):
      if type(path) == str:
         directories.append(path)
      else:
         directories = path.copy()
   
   # if all the elements in path are directories, and recursive is false, we list all the files in the directories list
   if all_obj_dir(path) and not recursive:
      for i in directories:
         directory = os.chdir(i)
         for j in os.listdir(directory):
            if j[0] == "." or j[0] == "_" or j[0] == "~":
               pass
            elif os.path.isdir(j):
               pass
            # if the file is a symbolic link, we skip it and display message "skipping non-regular file"
            elif os.path.islink(j) and not args.quiet:
               print("skipping non-regular file")
               pass
            else:
               files[j] = [os.getcwd(), os.stat(j).st_size, os.stat(j).st_mtime, os.stat(j).st_mode]
   
   # we store the base directories in a list
   base_directories = []
   
   # now the recursive part
   if recursive:
      
      # we create a list of files, that we will use to store the files in the directories
      files_list = []
      
      
      # for each directory in the directories list, we list the files in the directory
      while len(directories) > 0:
         
         # we change the current directory to the first directory in the list
         os.chdir(directories[0])
         directory = os.getcwd()
         
         # we add the directory to the list of base directories if it's in the path
         if directories[0] in path:
            base_directories.append(directory)
         
         # for each element in the directory, we add it to the files list if it's a file, or to the directories list if it's a directory
         for j in os.listdir(directory):
            
            # if the file is a hidden file, we skip it
            if j[0] == "." or j[0] == "_" or j[0] == "~":
               pass
            
            # if the file is a symbolic link, we skip it and display message "skipping non-regular file"
            elif os.path.islink(j) and not args.quiet:
               print("skipping non-regular file")
               pass
            
            # if the file is a directory, we add it to the directories list
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