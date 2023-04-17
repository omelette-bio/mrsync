import pickle, os

"""
message.py

deux fonctions:
=> send(fd,tag,v)
=> receive(fd)

fd : file descriptor to send/receive on
tag : string (tag of the message)
v : value (can be anything)

receive => return (tag,v) corresponding to what has been sent

Pour réaliser ces fonctions, nous utilisons os.read et os.write, mais aussi pickle.dumps et pickle.loads pour passer d’une valeur Python à une suite d’octets1, et enfin les méthodes from_bytes et to_bytes de la classe int pour convertir un entier Python en une représentation de cet entier sur 3 octets (pour donner dans l’en-tête la taille du message). Cela limite la taille d’un message à 23x8 octets, soit 16 Mo

"""

def send(fd,tag,v):
   s = pickle.dumps(v)
   n = len(s)
   os.write(fd, n.to_bytes(3, byteorder='big'))
   os.write(fd, tag.encode())
   os.write(fd, s)

fd = os.open("fifo", os.O_WRONLY)