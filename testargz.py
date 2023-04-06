import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-p", type=int, help="jsp")

args = parser.parse_args()

print(args.p)