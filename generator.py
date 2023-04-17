
def compare(a, b):
   list_to_send = []
   list_to_modify = []
   for i in a:
      if i in b:
         if a[i][2] > b[i][2]:
            list_to_modify.append(i)
      else:
         list_to_send.append(i)
   return list_to_send, list_to_modify