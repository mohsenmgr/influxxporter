from threading import Event,Thread
from backup_thread import BackUpThread
from compress_thread import CompressThread
from file_manager import FileManager
from influx_client import InfluxClient
from utils_cls import MyUtils
from mailer_cls import Mailer
from thread_interface import ThreadInterface
from utils_cls import MyUtils

class OperationManager():
    
    _instance = None

    def __new__(opman, *args, **kwargs):
        if opman._instance is None:
            opman._instance = super().__new__(opman)
        return opman._instance

    def __init__(self,fileMan:FileManager,mailerInstance:Mailer,influxClient:InfluxClient,utilsInstance):
        super().__init__()
        self.operation_dic = {
            'BACKUP_COMPRESS_EMAIL' : 'BACKUP_COMPRESS_EMAIL',
            'BACKUP_DOWNLOAD' : 'BACKUP_DOWNLOAD',
            'NO_OP' : 'NO_OP'
        }
        self.operationName = None
        self.operationThread:ThreadInterface = None
        self.fileManager:FileManager = fileMan
        self.mailer: Mailer = mailerInstance
        self.tables = None
        self.initDate = None
        self.finalDate = None
        self.influxClient: InfluxClient = influxClient
        self.utils:MyUtils = utilsInstance
        self.endUserEmail = None
        self.zipFileName = "archive"
        self.zipFilePath = None

    def set_tables(self,tables):
        self.tables = tables

    def set_date_tuple(self, tuple):
        self.initDate = tuple[0]
        self.finalDate = tuple[1]

    def set_end_user_email(self,email):
        self.endUserEmail = email


    def get_current_operation_Thread(self):
        return self.operationThread

    def set_current_operation(self,operationName):
        if operationName not in self.operation_dic:
            raise Exception(f"The operation '{operationName}' does not exist.")

        self.operationName = operationName

    def get_current_operation_name(self):
        return self.operationName

    def startOperation(self):
        if self.operationName == 'BACKUP_COMPRESS_EMAIL':
            res = self.utils.deleteAllFilesInDirectory()
            print(f"result of deletionAll: {res}")

            self.operation_Backup()
            self.operation_Compress()
            self.operation_Email()

        elif self.operationName == 'BACKUP_DOWNLOAD':
           self.operation_Backup()


    def operation_Backup(self):
        self.operationThread = BackUpThread(self.tables,self.fileManager,self.initDate,self.finalDate,self.influxClient,self.utils.getMainFilesDirectory())
        self.operationThread.start()

    def operation_Compress(self):
        oprationBacup:BackUpThread = self.operationThread
        if oprationBacup.getBusyFlag():
            oprationBacup.join()

        csvFiles = self.utils.listCsvFilesInDirectory()
        self.operationThread = CompressThread(self.utils.getMainFilesDirectory(),self.utils.getMainFilesDirectory(),csvFiles,self.zipFileName)
        self.operationThread.start()
        self.operationThread.join()
        self.zipFilePath = self.operationThread.getZipFilePath()

    def operation_Email(self):
        oprationCompress:CompressThread = self.operationThread
        if oprationCompress.getBusyFlag():
            oprationCompress.join()

        if self.utils.checkIfFileExistsInPath(self.zipFilePath):
            raise FileNotFoundError(f"The file '{self.zipFilePath}' does not exist.")
        print(f"result of checkIfZip Exists: {self.zipFilePath}")

        if self.endUserEmail and self.endUserEmail !="":
            self.mailer.send_email(self.endUserEmail,"SACHIM Measurement","Buongiorno, in allegato puoi trovare la misura richiesta.",self.zipFilePath)
        else:
            raise Exception("Email is not Set")
        
        self.utils.deleteOneFileInDirectory(self.zipFileName)
        self.utils.deleteAllFilesInDirectory()

    def halt_and_gracefully_kill(self):
        self.operationThread.setKillSwitch()
        self.operationThread.join()
        self.operationThread.unsetKillSwitch()






