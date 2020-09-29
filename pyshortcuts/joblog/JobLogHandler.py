
import platform
import socket

from .JobLog import JobLog
from .JobLogRequest import JobLogRequest


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

class JobLogHandler:

    def __init__(self, database, tableName, actions):

        self.actions = actions(database, tableName)

    def __call__(self, request):

        jobName = request.getJobName()

        if not isinstance(request, JobLogRequest):
            raise Exception("Expected @request to be an instance of JobLogInvokeRequest")

        if request.getIsSingleton():
            if self.actions.jobIsRunning(jobName):
                raise Exception("Job %s is already in progress!" % jobName)

        jobId = self.actions.startJob(
            jobName,
            get_ip()
        )

        if jobId < 0:
            raise Exception("Job %s could not be marked as started" % jobName)

        return JobLog(jobId, self.actions.finishJob)

