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

def _parseCommandLine(arguments):
	parser = argparse.ArgumentParser()

	for argument in arguments:
		shortName = argument.getShortName()
		longName = argument.getLongName()

		splat = {  }

		if argument.isFlag():
			splat["action"] = "store_true"
		else:
			splat["action"] = "store"

		if shortName is None and longName is not None:
			parser.add_argument("--" + longName, **splat)
		elif shortName is not None and longName is None:
			parser.add_argument("-" + shortName, **splat)
		else:
			parser.add_argument("-" + shortName, "--" + longName, **splat)

	cl_args, unknown_cl_args = parser.parse_known_args(sys.argv[1:])

	return cl_args.__dict__

def _parseEnvironmentVariables(expectedArguments):

	env_args = { }

	for expectedArgument in expectedArguments:
		
		if expectedArgument.getEnvironmentVariableName() is None:
			continue

		if type(expectedArgument.getEnvironmentVariableName()) == type(True):
			env_name = expectedArgument.getLongName()
		else:
			env_name = expectedArgument.getEnvironmentVariableName()

		if env_name in os.environ:
			env_args[expectedArgument.getLongName()] = os.environ[env_name]

	return env_args

def _parseDefaultValues(args):

	default_args = { }

	for expectedArgument in args:
		default_args[expectedArgument.getLongName()] = expectedArgument.getDefaultValue()

	return default_args

def _mergeArgs(mergeTo, mergeFrom):

	for key, value in mergeFrom.items():

		if key in mergeTo and mergeTo[key] is None:
			mergeTo[key] = value

	return


class ExpectedArgument:
	def __init__(self, defaultValue, shortName, longName, environmentVariableName, flag=False):
		self.defaultValue = defaultValue
		self.shortName = shortName
		self.longName = longName
		self.environmentVariableName = environmentVariableName
		self.flag = flag

	def getDefaultValue(self):
		return self.defaultValue

	def getShortName(self):
		return self.shortName

	def getLongName(self):
		return self.longName

	def getEnvironmentVariableName(self):
		return self.environmentVariableName
	
	def isFlag(self):
		return self.flag == True

class GetCommandLineArguments:

	functors = [ _parseCommandLine, _parseEnvironmentVariables, _parseDefaultValues ]

	def __init__(self, *expectedArguments):

		self.expectedArguments = expectedArguments
		self.emptyArguments = { }

		for expectedArgument in expectedArguments:
			if not isinstance(expectedArgument, ExpectedArgument):
				raise Exception('Must be an instance of ExpectedArgument')

			self.emptyArguments[expectedArgument.getLongName()] = None

	def __call__(self):

		emptyArguments = self.emptyArguments.copy()

		for functor in self.functors:

			functorArguments = functor(self.expectedArguments)
			_mergeArgs(emptyArguments, functorArguments)

		return emptyArguments