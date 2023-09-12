import threading

class FileManager:

    _instance = None

    def __new__(fm):
        if fm._instance is None:
            fm._instance = super().__new__(fm)
        return fm._instance

    def __init__ (self):
        self.files = []
        self.currentFile = None
        self.currentFile_lock = threading.Lock()
        self.totalFilesNumber = 0
        self.totalFilesNumber_lock = threading.Lock()

    def add_file(self, file):
        self.files.append(file)

    def get_all_files(self):
        return self.files
    
    def set_current_file(self, file):
        with self.currentFile_lock:
            self.currentFile = file

    def get_current_file(self):
        with self.currentFile_lock:
            return self.currentFile
    
    def set_totalNumber(self, number):
        with self.totalFilesNumber_lock:
            self.totalFilesNumber = number
   
    def get_totalNumber(self):
        with self.totalFilesNumber_lock:
            return self.totalFilesNumber