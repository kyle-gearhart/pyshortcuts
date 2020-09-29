# Copyright (c) 2020, Kyle A Gearhart
# Licensed under GPLv2

from .conn import openDbConnection as openDb
from pyshortcuts.cl.getcl import ExpectedArgument, GetCommandLineArguments


def OpenDbConnection(platform):
	
	args = GetCommandLineArguments( 
		ExpectedArgument(None, "D", "db_host", "DBHOST"),
		ExpectedArgument(3306, "p", "db_port", "DBPORT"),
		ExpectedArgument(None, "u", "db_user", "DBUSER"),
		ExpectedArgument(None, "x", "db_password", "DBPASSWORD"),
		ExpectedArgument(None, "n", "db_name", "DBNAME"),
		ExpectedArgument(None, "H", "ssh_host", "SSHHOST"),
		ExpectedArgument(None, "P", "ssh_port", "SSHPORT"),
		ExpectedArgument("ubuntu", "U", "ssh_user", "SSHUSER"),
		ExpectedArgument(None, "K", "ssh_pkey", "SSHPKEY")
	)
	
	return openDb(platform, args())