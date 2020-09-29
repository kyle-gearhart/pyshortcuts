# Copyright (c) 2018, Kyle A Gearhart
# Licensed under GPLv2

# Callers should import openDbConnection and put shutdownDbTunnels in a 
# finally block.

# Expects the following properties for a database connection:
#		db_host
#		db_port
#		db_user
#		db_password
#		db_name

# Expects the following @properties for a tunneled connection:
#		ssh_host
#		ssh_port
#		ssh_user
#		ssh_pkey
#

import copy
import pymysql.cursors
import random
import signal

from sshtunnel import SSHTunnelForwarder
from pyshortcuts.cl.getcl import parseArguments as parse_cl_args 

def _openDbMySql(properties):

	conn_args = {
		"host": properties["db_host"],
		"port": int(properties["db_port"]),
		"user": properties["db_user"],
		"password": properties["db_password"],
		"db": properties["db_name"],
		"cursorclass": pymysql.cursors.DictCursor
	}

	try:
		connection = pymysql.connect(**conn_args)
	except:
		raise Exception("Could not connect to MySQL with the desired connection string")

	return connection


_platformMap = {
	"mysql": _openDbMySql
}

_openTunnels = []
_openConnections = []

_signalSet = False

def openDbClArgs():

	return [
		[ None, "D", "db_host", False, "DBHOST"],
		[ 3306, "p", "db_port", False, "DBPORT"],
		[ None, "u", "db_user", False, "DBUSER"],
		[ None, "x", "db_password", False, "DBPASSWORD"],
		[ None, "n", "db_name", False, "DBNAME"],
		[ None, "H", "ssh_host", False, "SSHHOST"],
		[ None, "P", "ssh_port", False, "SSHPORT"],
		[ "ubuntu", "U", "ssh_user", False, "SSHUSER"],
		[ None, "K", "ssh_pkey", False, "SSHPKEY"]
	]

def openDbConnectionFromCLArgs(platform):
	
	args = parse_cl_args(openDbClArgs())
	
	
	return openDbConnection(platform, args)

def openDbConnection(platform, properties):

	if platform not in _platformMap:
		raise Exception("Platform %s not recognized, valid platforms are: %s" % (platform, _platformMap.keys()))

	functor = _platformMap[platform]	
	tunnelProperties = _handleTunnel(properties)
	
	connection = functor(tunnelProperties)

	if connection:
		_openConnections.append(connection)

	return connection

def closeDbTunnels():

	for tunnel in _openTunnels:
		tunnel.stop()

	return

def closeDbConnections():
	
	for connection in _openConnections:
		print("Will not shut down")

	return	

def _handleTunnel(properties):

	tunnelProperties = copy.deepcopy(properties)

	if "ssh_host" in properties and properties["ssh_host"] is not None:
		
		_setSignal()
		
		localBindPort = random.randint(12000, 12999)
		
		tunnel_args = {
			"ssh_username": tunnelProperties["ssh_user"],
			"ssh_pkey": tunnelProperties["ssh_pkey"],
			"remote_bind_address": (tunnelProperties["db_host"], int(tunnelProperties["db_port"])),
			"local_bind_address": ("127.0.0.1", localBindPort)
		}


		tunnel = SSHTunnelForwarder((tunnelProperties["ssh_host"], int(tunnelProperties["ssh_port"])), **tunnel_args)
		tunnel.start()
		
		tunnelProperties["db_host"] = "127.0.0.1"
		tunnelProperties["db_port"] = localBindPort

		_openTunnels.append(tunnel)

	return tunnelProperties

def _handleSignal(signum, frame):
	closeDbConnections()
	closeDbTunnels()
	
	return

def _setSignal():

	global _signalSet

	if not _signalSet:
		signal.signal(signal.SIGINT, _handleSignal)
		_signalSet = True

	return

