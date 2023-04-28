def order_list_delete(list_to_delete):
   # we need to delete the files from the deepest folder to the highest
   # so we sort the list by the number of / in the path
   for i in range(len(list_to_delete)):
      for j in range(len(list_to_delete)):
         if list_to_delete[i].count("/") > list_to_delete[j].count("/"):
            list_to_delete[i], list_to_delete[j] = list_to_delete[j], list_to_delete[i]
   return list_to_delete