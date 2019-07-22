


class JobTableActions:

    def __init__(self, database, tableName):

        self.database = database
        self.tableName = tableName

    def jobIsRunning(self, jobName):

        sql = """SELECT * FROM %s 
            WHERE job_name = %s
                AND job_running = 1"""

        with self.database.cursor() as c:
            rows = c.execute(sql, (self.tableName, jobName))

            if rows:
                return True
        
        return False

    def startJob(self, jobName, jobPlatform):

        sql = """INSERT INTO %s ( 
            job_name, 
            job_started, 
            job_running,
            job_platform ) VALUES (
                %s,
                NOW(),
                1,
                %s
            )"""
        print sql

        with self.database.cursor() as c:
            c.execute(sql, (self.tableName, jobName, jobPlatform))
            return c.lastrowid
        
        return -1

    def finishJob(self, jobId, success, message):

        sql = """UPDATE %s
            SET job_finished = NOW(),
                job_running = 0,
                job_successs = %s,
                job_message = %s
            WHERE job_id = %s"""

        with self.database.cursor() as c:
            c.execute(sql, (self.tableName, success, message, jobId))
            return True

        return False