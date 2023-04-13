import options, sys, sender

args = options.parsing()
sender.send_files(args.source, args)

sys.exit(0)