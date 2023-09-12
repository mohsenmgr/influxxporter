import threading
import csv
from datetime import datetime, timezone
from file_cls import FileObject
from file_manager import FileManager
from influx_client import InfluxClient
from influxdb import InfluxDBClient
from thread_interface import ThreadInterface


class BackUpThread(ThreadInterface,threading.Thread):
    def __init__(self,tables,manager,initDate,finalDate,client:InfluxClient,uploadFolder):
        ThreadInterface.__init__(self)
        threading.Thread.__init__(self)
        self.tables = []
        self.setTables(tables=tables)
        self.manager: FileManager = manager
        self.set_date_tuple(initialData=initDate,finalData=finalDate)
        self.influxClient:InfluxDBClient = client.get_influxDbInstamce()
        self.uploadFolder = uploadFolder


    def sanitizeCsvFileName(self,csvFileName):
        result = ""
        replacement_dict = {
            ' ' : '_',
            ':' : '',
            "(" : "",
            ")" : "",
            "+" : "",
            "/" : "",
            "\"" : "",
            "\'" : ""
        }
        for char in csvFileName:
       
            if char in replacement_dict:
                result += replacement_dict[char]
            else:
                result += char

        return result

    def setUploadFolder(self,upFolder):
        self.uploadFolder = upFolder

    def setTables(self,tables):
        for table in tables:
            table = "\"" + table + "\""
            self.tables.append(table)


    def validate_date_format(self,dates):
        for date in dates:
            try:
                datetime.strptime(date, '%Y-%m-%d')       
            except ValueError:
                return False
        return True 

    def set_date_tuple(self,initialData,finalData):
        
        if not self.validate_date_format((initialData,finalData)):
            raise ValueError("The date '{date_string}' is not in the correct format ('%Y-%m-%d').")

        self.initialDate = self.dateConverter(initialData)
        self.finalDate = self.dateConverter(finalData)

    def dateConverter(self,dateString):
        dateString = dateString + 'T00:00:00.000Z'
        date_obj = datetime.strptime(dateString, '%Y-%m-%dT%H:%M:%S.%fZ')
        utc_timestamp = date_obj.replace(tzinfo=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return utc_timestamp 

    def run(self):
        
        self.setBusyFlag(True)
        idx = 0
        for table in self.tables:
            if self.kill_switch.is_set():
                break
            
            idx = idx + 1
            file = FileObject(idx,table)
            self.manager.add_file(file)
            
            query = f"SELECT * FROM {table} WHERE time >= '{self.initialDate}' and time < '{self.finalDate}';"

            # Execute the query
            result = self.influxClient.query(query)

            # Define the CSV file name
            csv_file_name = self.uploadFolder + self.sanitizeCsvFileName(table) + ".csv"

            # Write the result to a CSV file
            with open(csv_file_name, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)

                # Write header row
                csv_writer.writerow(result.raw['series'][0]['columns'])

                # Write data rows
                for row in result.raw['series'][0]['values']:
                    csv_writer.writerow(row)

            print(f"Data {csv_file_name} exported to {csv_file_name}")
            self.manager.set_current_file(file)

        print("ALL TABLES EXPORTED")
        self.setBusyFlag(False)
