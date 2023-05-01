import pickle, os, select

def send(fd,tag,v):
   """send a message on fd"""
   try:
      # encode tag size on 3 Bytes
      tag_size = len(tag)
      # write tag size and tag
      os.write(fd,tag_size.to_bytes(3,"big"))
      os.write(fd,tag.encode())
      # encode message
      msg = pickle.dumps(v)
      # encode message size on 4 Bytes
      size = len(msg)
      # write message size and message
      os.write(fd,size.to_bytes(4,"big"))
      os.write(fd,msg)
      return True
   except:
      return False

def receive(fd):
   """receive a message on fd"""
   try:
      # read tag size and tag
      tag_size = int.from_bytes(os.read(fd,3),"big")
      tag = os.read(fd,tag_size).decode()
      # read message size and message
      size = int.from_bytes(os.read(fd,4),"big")
      msg = os.read(fd,size)
      # return tag and message
      return tag,pickle.loads(msg)
   except:
      return "received-nothing",[]
