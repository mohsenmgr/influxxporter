class FileObject:
    def __init__(self,fileNumber,fileName):
        self.fileNumer = fileNumber
        self.fileName = fileName

    def getFileName(self):
        return self.fileName

    def getFileNumber(self):
        return self.fileNumer