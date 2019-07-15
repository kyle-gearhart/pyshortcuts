# Copyright (c) 2018, Kyle A Gearhart
# Licensed under GPLv2


# Returns a dictionary containing key value pairs, sourced from
#		1)	Command line arugments
#		2)	Environment variables
#		3) Default values
#
# The caller should provide a List with all keys to be processed.
# Each key shall contain a list object representing the following items
#		1)	Default value
#		2)	Short Option Name
#		3) Long Option Name
#		4) True/False indicating if this is a flag variable
#		5) Environment variable name (True if the same as Long Option Name, None
#			if an environment variable should not be searched for)
#
# For an example, an input file name may look something like this:
#		[ "input.csv", "INPUT", "i", False, None ]
#
# An API key may look something like this:
#		[ None, "APIKEY", "k", False, "STRIPE_API_KEY" ]


import argparse
import os
import sys


DEFAULT_VALUE = 0
SOPT_NAME = 1
LOPT_NAME = 2
IS_FLAG = 3
ENV_NAME = 4


def createArgument(defaultValue, shortName, longName, flag, environmentName):
	
	return [ defaultValue, shortName, longName, flag, environmentName]


def parseArguments(args):

	functors = [ _parseCommandLine, _parseEnvironmentVariables, _parseDefaultValues ]

	parsed_args = _createEmptyArgs(args)

	for functor in functors:

		functor_args = functor(args)
		_mergeArgs(parsed_args, functor_args)

	return parsed_args


def _parseCommandLine(args):
	parser = argparse.ArgumentParser()

	for argument in args:
		short_name = argument[SOPT_NAME]
		long_name = argument[LOPT_NAME]

		splat = {  }

		if argument[IS_FLAG]:
			splat["action"] = "store_true"
		else:
			splat["action"] = "store"

		if short_name is None and long_name is not None:
			parser.add_argument("--" + long_name, **splat)
		elif short_name is not None and long_name is None:
			parser.add_argument("-" + short_name, **splat)
		else:
			parser.add_argument("-" + short_name, "--" + long_name, **splat)

	cl_args, unknown_cl_args = parser.parse_known_args(sys.argv[1:])

	return cl_args.__dict__

def _parseEnvironmentVariables(args):

	env_args = { }

	for argument in args:
		
		if argument[ENV_NAME] is None:
			continue

		if type(argument[ENV_NAME]) == type(True):
			env_name = arugment[LOPT_NAME]
		else:
			env_name = argument[ENV_NAME]

		if env_name in os.environ:
			env_args[argument[LOPT_NAME]] = os.environ[env_name]

	return env_args

def _parseDefaultValues(args):

	default_args = { }

	for argument in args:
		default_args[argument[2]] = argument[0]

	return default_args

def _createEmptyArgs(args):

	empty_args = { }

	for argument in args:
		empty_args[argument[LOPT_NAME]] = None

	return empty_args

def _mergeArgs(mergeTo, mergeFrom):

	for key, value in mergeFrom.iteritems():

		if key in mergeTo and mergeTo[key] is None:
			mergeTo[key] = value

	return

