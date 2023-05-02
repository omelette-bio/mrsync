import filelist

# Return a list of files and directories
def list_files(path, arguments):
   # if the user wants to archive the files, we need to list the files recursively
   recursive = arguments.recursive | arguments.archive
   file_list = filelist.list_files(path, arguments, recursive)
   return file_list

# return a boolean value if the path contains only directories
def all_path_dir(path):
   return filelist.all_obj_dir(path)

