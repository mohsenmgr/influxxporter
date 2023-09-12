from threading import Event,Thread

class ThreadManager():
    
    _instance = None

    def __new__(tman):
        if tman._instance is None:
            tman._instance = super().__new__(tman)
        return tman._instance

    def __init__(self):
        super().__init__()
        self.threadNumber = 0

        self.threads = []
        self.threadEvents = []


    def createThread(self, func, *args, **kwargs):
        self.threadNumber = self.threadNumber + 1

        myEvent = Event()
        self.threadEvents.append(myEvent)
        myThread = Thread(name=f"non-blocking{self.threadNumber}",target=func,args=args,kwargs=kwargs)
        self.threads.append(myThread)
        myThread.start()
        return myThread
    
    def stopAll(self):
        for ev in self.threadEvents:
            print("stopping thread")
            print(ev)
            ev.set()

        for worker in self.threads:
            worker.join()
