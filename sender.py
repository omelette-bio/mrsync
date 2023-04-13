import filelist

def send_files(path, arguments):
   file_list = filelist.list_files(path, arguments.recursive)
   if arguments.list_only:
      print("Files to send: ")
      for i in file_list:
         print("* " + i)
