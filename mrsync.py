import options, sys

args = options.parsing()
if args.list_only: options.listing(args.source)

sys.exit(0)