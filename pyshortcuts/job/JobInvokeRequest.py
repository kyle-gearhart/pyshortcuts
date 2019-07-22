


class JobInvokeRequest:
    def __init__(self, JobName, Singleton):

        if not isinstance(JobName, basestring):
            raise Exception("Invalid job name")

        if not isinstance(Singleton, bool):
            raise Exception("Expected boolean for @Singleton")

        self.Singleton = Singleton
        self.JobName = JobName

    def getJobName(self):

        return self.JobName

    def getIsSingleton(self):

        return self.Singleton
        