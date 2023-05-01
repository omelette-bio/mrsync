import filelist

def list_files(path, arguments):
   recursive = arguments.recursive | arguments.archive
   file_list, dirs = filelist.list_files(path, arguments, recursive)
   return file_list, dirs

def all_path_dir(path):
   return filelist.all_obj_dir(path)

