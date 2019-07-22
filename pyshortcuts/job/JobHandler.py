
from Job import Job
from JobInvokeRequest import JobInvokeRequest

class JobHandler:

    def __init__(self, database, tableName, actions):

        self.actions = actions(database, tableName)

    def __call__(self, request):

        if not isinstance(request, JobInvokeRequest):
            raise Exception("Expected @request to be an instance of JobInvokeRequest")
            
        if request.getSingleton():
            if self.actions.jobIsRunning(request.getJobName()):
                raise Exception("Job %s is already in progress!" %(request.getJobName()))

        jobId = self.actions.startJob(request.getJobName())

        return Job(jobId, self.actions.finishJob)

