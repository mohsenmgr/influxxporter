import threading


class ThreadInterface:
    def __init__(self):
        self.kill_switch: threading.Event = threading.Event()
        self.busy_flag = False


    def unsetKillSwitch(self):
        print("kill Switch deactivated")
        self.kill_switch.clear()

    def setKillSwitch(self):
        print("kill Switch active")
        self.kill_switch.set()
    
    def setBusyFlag(self,flag):
        self.busy_flag = flag

    def getBusyFlag(self):
        return self.busy_flag