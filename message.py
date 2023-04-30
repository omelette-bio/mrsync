import pickle, os, select

def send(fd,tag,v):
   """send a message on fd"""
   try:
      tag_size = len(tag)
      os.write(fd,tag_size.to_bytes(3,"big"))
      os.write(fd,tag.encode())
      msg = pickle.dumps(v)
      size = len(msg)
      #encode message size on 16 Mo
      os.write(fd,size.to_bytes(4,"big"))
      os.write(fd,msg)
      return True
   except:
      return False

def receive(fd):
   try:
      tag_size = int.from_bytes(os.read(fd,3),"big")
      tag = os.read(fd,tag_size).decode()
      size = int.from_bytes(os.read(fd,3),"big")
      msg = os.read(fd,size)
      return tag,pickle.loads(msg)
   except:
      return "received-nothing",[]
