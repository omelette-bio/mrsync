import argparse


parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()

group.add_argument("-v", "--verbose", action="count", help="increase output verbosity")
group.add_argument("-q", "--quiet", help="suppress non-error messages")

parser.add_argument("-a","--archive", help="archive mode")
parser.add_argument("-r","--recursive", help="recurse into directories")
parser.add_argument("-u","--update", help="skip files that are newer on the receiver")
parser.add_argument("-d","--dirs", help="transfer directories without recursing")
parser.add_argument("-H","--hard-links", help="preserve hard links")
parser.add_argument("-p","--perms", help="preserve permissions")
parser.add_argument("-t","--times", help="preserve times")
parser.add_argument("--existing", help="skip creating new files on receiver")
parser.add_argument("--ignore-existing", help="skip updating files that exist on receiver")
parser.add_argument("--delete", help="delete extraneous files from dest dirs")
parser.add_argument("--force", help="force deletion of dirs even if not empty")
parser.add_argument("--timeout", type=int, help="set I/O timeout in seconds")
parser.add_argument("--blocking-io", help="use blocking I/O for the remote shell")
parser.add_argument("-I","--ignore-times", help="don't skip files that match in size and time")
parser.add_argument("--size-only", help="skip files that match in size")
parser.add_argument("--port", type=str, help="specify double-colon alternate port number")
parser.add_argument("--list-only", help="list the files instead of copying them")

#commands to run with daemon
parser.add_argument("--daemon", help="run as an mrsync daemon")
parser.add_argument("--address", type=str, help="bind to the specified address")
parser.add_argument("--no-detach", help="do not detach from the parent")
parser.add_argument("--port=PORT", help="listen on alternate port number")

parser.parse_args()