# Copyright (c) 2020, Kyle A Gearhart
# Licensed under GPLv2

from .conn import openDbConnection as openDb
from pyshortcuts.cl.getcl import ExpectedArgument, GetCommandLineArguments


def OpenDbConnection(platform):
	
	args = GetCommandLineArguments( 
		ExpectedArgument(None, "D", "db_host", False, "DBHOST"),
		ExpectedArgument(3306, "p", "db_port", False, "DBPORT"),
		ExpectedArgument(None, "u", "db_user", False, "DBUSER"),
		ExpectedArgument(None, "x", "db_password", False, "DBPASSWORD"),
		ExpectedArgument(None, "n", "db_name", False, "DBNAME"),
		ExpectedArgument(None, "H", "ssh_host", False, "SSHHOST"),
		ExpectedArgument(None, "P", "ssh_port", False, "SSHPORT"),
		ExpectedArgument("ubuntu", "U", "ssh_user", False, "SSHUSER"),
		ExpectedArgument(None, "K", "ssh_pkey", False, "SSHPKEY")
	)
	
	return openDb(platform, args())