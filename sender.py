import filelist, os

def list_files(path, arguments):
   file_list = filelist.list_files(path, arguments.recursive)
   return file_list