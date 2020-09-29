import csv
import getopt
import sys

def read_csv(inputFile, fields, delimiter=None, **kwargs):

	csvopts = { "delimiter": delimiter if delimiter else "," }
	rows = []

	with open(inputFile, 'r') as f:
		r = csv.reader(f, **csvopts)

		for row in r:
			out = []

			for idx in fields:
				out.append(row[idx])

			rows.append(out)

	return rows


args = { "outputFile": None, "fields": None, "inputFile": None }
arg_map = {
	"outputFile": "O",
	"fields": "F",
	"inputFile": "I" }

try:
	opts, oargs = getopt.getopt(sys.argv[1:], "O:F:I:", [ "outputFile", "fields", "inputFile" ])
except getopt.GetoptError as err:
	print(str(err))
	sys.exit(2)

cmd_opts = dict(opts)

for map_key, map_value in arg_map.items():
	opt_keys = ["-" + map_value, "--" + map_key]

	for opt_key in opt_keys:
		if opt_key in cmd_opts:
			print(args)
			print(cmd_opts)
			args[map_key] = cmd_opts[opt_key]

if args["fields"]:
	args["fields"] = [int(x) for x in args["fields"].split(',')]

with open(args["outputFile"], 'w') as o:
	csvwriter = csv.writer(o)
	rows = read_csv(**args)

	for row in rows:
		csvwriter.writerow(row)

		
