
import pymysql.cursors

__EXECUTEMANY = "executeMany"

def insertRecords(conn, table, fields, records, prefix_cols):		

	sql = "INSERT INTO " + table + " ("
	first = True
	data = []

	for field in fields:
		if first:
			first = False
		else:
			sql += ", "

		sql += table + "_" + field
	
	sql += ") VALUES ("
	
	first = True
	for field in fields:
		if first:
			first = False
		else:
			sql += ", "

		sql += "%s"

	sql += ")"

	for record in records:

		rec = []

		for field in fields:	
			if prefix_cols:
				record_fname = table + "_" + field
			else:
				record_fname = field

			rec.append(record[record_fname])

		data.append(tuple(rec))

	return __execute(__EXECUTEMANY, conn, sql, data)


def __execute(style, connection, sql, data):

	functors = __getFunctorTable(connection)

	if style not in functors:
		raise Exception("Database execution style %s not supported by the underlying database connection" % (style))

	return functors[style](connection, sql, data)

def __getFunctorTable(connection):

	if isinstance(connection, pymysql.connections.Connection):

		return {
			__EXECUTEMANY: __mysqlExecuteMany
		}

	raise Exception("Database connection object not recognized")

def __mysqlExecuteMany(connection, sql, data):
	
	with connection.cursor() as cursor:
		cursor.executemany(sql, data)
		connection.commit()

	return True

