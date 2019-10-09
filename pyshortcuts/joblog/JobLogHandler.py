
import platform

from JobLog import JobLog
from JobLogInvokeRequest import JobLogInvokeRequest

class JobLogHandler:

    def __init__(self, database, tableName, actions):

        self.actions = actions(database, tableName)

    def __call__(self, request):

        jobName = request.getJobName()

        if not isinstance(request, JobLogInvokeRequest):
            raise Exception("Expected @request to be an instance of JobLogInvokeRequest")

        if request.getIsSingleton():
            if self.actions.jobIsRunning(jobName):
                raise Exception("Job %s is already in progress!" % jobName)

        jobId = self.actions.startJob(jobName,
            platform.node())

        if jobId < 0:
            raise Exception("Job %s could not be marked as started" % jobName)

        return JobLog(jobId, self.actions.finishJob)

