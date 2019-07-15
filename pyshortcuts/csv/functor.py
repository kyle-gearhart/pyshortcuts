# Copyright (c) 2018, Kyle A Gearhart
# Licensed under GNU GPLv2

import csv
import os


def readRows(file_name, reader_opts, 
				 row_function, row_function_args, 
				 chunk_size, 
				 chunk_function, chunk_function_args):

	keep_running = True

	reader_opts = _assignDefaultProperties(reader_opts)

	with open(file_name, "r") as f:
		reader = csv.reader(f, **reader_opts)
		
		for i, row in enumerate(reader):
			row_function(row, **row_function_args)

			if chunk_size > 0 and i % chunk_size == 0:
				keep_running = chunk_function(**chunk_function_args)

				if not keep_running:
					break

		if chunk_size > 0:
			keep_running = chunk_function(**chunk_function_args)

	return keep_running

def _assignDefaultProperties(options):

	default_options = {
		"delimiter": ","
	}

	if options is None:
		return default_options

	for key, value in default_options:
		if key not in options:
			options[key] = value

	return options

