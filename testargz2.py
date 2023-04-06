import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-p",type=int,help="port")

def parsing():
   return parser.parse_args()