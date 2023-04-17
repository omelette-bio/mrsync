import pickle, os

def send(fd,tag,v):
   """send a message on fd"""
   msg = pickle.dumps(v)
   size = len(msg)
   tag_size = len(tag)
   os.write(fd,tag_size.to_bytes(3,"big"))
   os.write(fd,tag.encode())
   os.write(fd,size.to_bytes(3,"big"))
   os.write(fd,msg)

def receive(fd):
   """receive a message on fd"""
   tag_size = int.from_bytes(os.read(fd,3),"big")
   tag = os.read(fd,tag_size).decode()
   size = int.from_bytes(os.read(fd,3),"big")
   msg = os.read(fd,size)
   return tag,pickle.loads(msg)
