class Job:
    def __init__(self, key, condition):
        self.key = key
        self.__dict__.update(condition)

class Registry:
    def __init__(self):
        self.queue_reset()

    def queue_reset(self):
        self.queue      = {}
        self.end_flag   = {}

    def flag_reset(self):
        for key in self.queue.keys():
            self.end_flag[key] = False

    def submit(self, job):
        if job.key in self.queue.keys():
            raise("This job key is already used")
        else:
            self.queue[job.key]     = job
            self.end_flag[job.key]  = False