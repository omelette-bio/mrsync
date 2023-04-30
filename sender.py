import filelist

def list_files(path, arguments):
   recursive = arguments.recursive | arguments.archive
   file_list = filelist.list_files(path, recursive)
   return file_list

