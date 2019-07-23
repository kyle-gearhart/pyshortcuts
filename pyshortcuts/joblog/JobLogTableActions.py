


class JobLogTableActions:

    def __init__(self, database, tableName):

        self.database = database
        self.tableName = tableName

    def jobIsRunning(self, jobName):

        sql = """SELECT * FROM """ + self.tableName + """
             WHERE job_name = %s
                AND job_running = 1"""

        with self.database.cursor() as c:
            rows = c.execute(sql, (jobName))

            if rows:
                return True
        
        return False

    def startJob(self, jobName, jobPlatform):

        sql = """INSERT INTO """ + self.tableName + """ ( 
            job_name, 
            job_started, 
            job_running,
            job_platform ) VALUES (
                %s,
                NOW(),
                1,
                %s
            )"""

        with self.database.cursor() as c:
            c.execute(sql, (jobName, jobPlatform))
            return c.lastrowid
        
        return -1

    def finishJob(self, jobId, success, message):

        sql = """UPDATE """ + self.tableName + """
             SET job_finished = NOW(),
                job_running = 0,
                job_success = %s,
                job_message = %s
            WHERE job_id = %s"""

        with self.database.cursor() as c:
            c.execute(sql, (success, message, jobId))
            self.database.commit()

            return True

        return False