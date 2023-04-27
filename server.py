import os
# function to create a list of folder to create in the destination folder

# if the path is not a folder, it will return an empty list

# if the path contains one folder, it will return an empty list
# if the path contains one folder and recursive is true, it will return only the subfolders

# if the path contains more than one folder, it will return a list of folders
# if recursive is true, it will return a list of folders and subfolders

def create_folder_list(path,recursive=False):
   folder_list = []
   for i in path:
      if os.path.isfile(i):
         continue
      elif os.path.isdir(i) and i[0] != "." and i[0] != "_" and i[0] != "~":
         folder_list.append(i)
         if recursive:
            for j in os.listdir(i):
               if os.path.isdir(j) and j[0] != "." and j[0] != "_" and j[0] != "~":
                  folder_list.append(os.path.join(i,j))
   return folder_list