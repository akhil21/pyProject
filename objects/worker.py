DEBUG_MODE = False

def set_debug_mode(mode):
    global DEBUG_MODE
    DEBUG_MODE = mode

class Worker:
    def __init__(self,registry,dataset,take_data=None):
        self.registry   = registry
        self.dataset    = dataset
        self.take_data  = take_data

    def execute_job(self,key):
        job                         = self.registry.queue[key]
        data                        = self.take_data(job)
        self.registry.end_flag[key] = True
        self.dataset.save(key, data)

        if DEBUG_MODE:
            self.report(key, data)

    def execute_all_job(self):
        for key in self.registry.queue.keys():
            self.execute_job(key)

    def report(self, key, data):
        print('\033[32m')
        print("Job ID : [{0}]".format(key))
        print(" "*5 + str(data))
        print('\033[0m')