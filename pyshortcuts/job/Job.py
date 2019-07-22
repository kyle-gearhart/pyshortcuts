
class Job:

    def __init__(self, jobId, finish):

        self.jobId = jobId
        self.finish = finish

    def __call__(self, success, message):

        if message is None:
            message = "Job finished"

        if not self.finish(self.jobId, success, message):
            raise Exception("JobId %s could not be finished" % (jobId, ))