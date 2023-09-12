import threading
from thread_interface import ThreadInterface
import py7zr


class CompressThread(ThreadInterface,threading.Thread):
    def __init__(self,csvFolderLocation,zipFilePath,csvFiles,archiveName):
        ThreadInterface.__init__(self)
        threading.Thread.__init__(self)

        self.csvFolderLocation = csvFolderLocation
        self.zipFilePath = zipFilePath
        self.csvFiles : [] = csvFiles
        self.archiveName = archiveName

    def getZipFilePath(self):
        filePath = f'{self.csvFolderLocation}{self.archiveName}.7z'
        return filePath

    def run(self):

        self.setBusyFlag(True)

        print("COMPRESSION STARTED")
        with py7zr.SevenZipFile(self.getZipFilePath(), 'w') as archive:
            for csv_file in self.csvFiles:
                if self.kill_switch.is_set():
                    break
                csv_file = self.csvFolderLocation + csv_file
                archive.write(csv_file)
        print("COMPRESSION Finished")

        self.setBusyFlag(False)
