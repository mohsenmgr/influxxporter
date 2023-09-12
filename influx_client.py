from influxdb import InfluxDBClient

class InfluxClient:

    _instance = None

    def __new__(infcl, *args, **kwargs):
        if infcl._instance is None:
            infcl._instance = super().__new__(infcl)
        return infcl._instance

    def __init__(self,hostname,port,dbName):
        self.hostName = hostname
        self.port = port
        self.databaseName = dbName
        self.influxDbClient = InfluxDBClient(host=self.hostName, port=self.port, database=self.databaseName)
        
    def get_influxDbInstamce(self):
        return self.influxDbClient