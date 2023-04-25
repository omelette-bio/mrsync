# function that returns a sorted dictionary of files following the path name 

def sort_by_path(dictionnary):
   return dict(sorted(dictionnary.items(), key=lambda x: x[1][0]))




# function to compare two lists of files and return the list of files to send, modify and delete
def compare(a, b):
   list_to_send = []
   list_to_modify = []
   list_to_delete = []
   for i in a:
      if i in b:
         if a[i][2] > b[i][2]:
            list_to_modify.append(i)
      else:
         list_to_send.append(i)
   for i in b:
      if i not in a:
         list_to_delete.append(i)
   return list_to_send, list_to_modify, list_to_delete