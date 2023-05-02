import os
# function that returns a sorted dictionary of files following the path name 

def sort_by_path(dictionnary):
   return dict(sorted(dictionnary.items(), key=lambda x: x[1][0]))




# function to compare two lists of files and return the list of files to send, modify and delete
def compare(a, b, args):
   list_to_send = []
   list_to_modify = []
   list_to_delete = []
   
   if len(args.source) == 1:
      for i in a:
         if i in b:
            if not args.ignore_existing:
               if args.size_only:
                  if a[i][1] != b[i][1]:
                     list_to_modify.append(i)
               
               elif args.ignore_times:
                  list_to_modify.append(i)
               
               else:
                  if a[i][2] == b[i][2] and a[i][1] == b[i][1]:
                     pass
                  # if --update is specified, we compare the modification time of the files, if the destination is older
                  elif args.update:
                     if a[i][2] > b[i][2]:
                        list_to_modify.append(i)
                  elif a[i][2] != b[i][2] or a[i][1] != b[i][1]:
                     list_to_modify.append(i)
                  elif args.perms or args.archive:
                     if a[i][3] != b[i][3]:
                        list_to_modify.append(i)
         else:
            if not args.existing:
               list_to_send.append(i)
      
      for i in b:
         if i not in a:
            list_to_delete.append(i)
   
   
   else:
      # if the source has multiple folders, we need to compare the files in the same folder
      # and create the relative path of the file
      for files in a:
         file = os.path.join(os.path.basename(a[files][0]),files)
         if file in b and not args.ignore_existing:
            # now reproduce the same process as above
            
            if args.size_only:
               if a[files][1] != b[file][1]:
                  list_to_modify.append(file)
            
            elif args.ignore_times:
               list_to_modify.append(file)
            
            else:
               if a[files][2] == b[file][2] and a[files][1] == b[file][1]:
                  pass
               elif a[files][2] > b[file][2] or a[files][1] > b[file][1]:
                  list_to_modify.append(file)
               elif args.perms or args.archive:
                  if a[files][3] != b[file][3]:
                     list_to_modify.append(file)
         elif not args.existing:
            list_to_send.append(file)
      # now check if there are files in the destination that are not in the source
      for files in b:
         if files not in a:
            list_to_delete.append(files)
         
      
      
   return list_to_send, list_to_modify, list_to_delete