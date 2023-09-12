from file_manager import FileManager
import sys
import atexit
from file_cls import FileObject
from flask import Flask, render_template, request, Response, jsonify, send_from_directory
from measure_filler import Populator
from mailer_cls import Mailer
from operation_man import OperationManager
from influx_client import InfluxClient
from utils_cls import MyUtils
import os

app = Flask(__name__)

targetDirectory = os.environ.get('BACKUP_DIR', './backup/')
measurementsInputFile = os.environ.get('TABLES_FILE','tables.txt')
smtp_address = os.environ.get('MAILER_SMTPS_ADDRESS','smtps.aruba.it')
smtp_port = os.environ.get('MAILER_SMTPS_PORT','465')
smtp_mailer_email = os.environ.get('MAILER_SENDER_MAIL','noreply@beeta.it')
smtp_mailer_password = os.environ.get('MAILER_SENDER_PASSWORD','*******')
influx_db_host = os.environ.get('INFLUX_HOST','localhost')
influx_db_port=  os.environ.get('INFLUX_PORT','8086')
influx_db_db_name = os.environ.get('INFLUX_DB_NAME','influx')

myUtils = MyUtils(targetDirectory)
fileManager = FileManager()
populator = Populator(measurementsInputFile)
mailer = Mailer(smtp_address,smtp_port,smtp_mailer_email,smtp_mailer_password)
inflxClient = InfluxClient(influx_db_host,influx_db_port,influx_db_db_name)
operationManager = OperationManager(fileManager,mailer,inflxClient,myUtils)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/files/current", methods=["GET"])
def files():
    totalFiles = fileManager.get_totalNumber()
    currentFile: FileObject = fileManager.get_current_file()

    if currentFile is not None:
        print(f"{currentFile=}")
        print(f"FileNumber: {currentFile.getFileName()}")
        print(f"FileName: {currentFile.getFileName()}")
    else: 
        print("current file is none")
        
    if(currentFile is None):
        return jsonify({
           "status": "waiting"
    })
    
    print(f"totalFiles {totalFiles}")
    print(f"currentFile {currentFile.getFileNumber()}")

    if currentFile.getFileNumber() != totalFiles:
       json = jsonify({
           "fileNumber": currentFile.getFileNumber(),
           "totalFiles": totalFiles,
           "fileName": currentFile.getFileName()
       })
    else:
       json = jsonify({
           "fileNumber": currentFile.getFileNumber(),
           "totalFiles": totalFiles,
           "fileName": currentFile.getFileName(),
           "status": "finished"
       }) 
       

    return json


@app.route('/api/measurements',methods=["GET"])
def get_measurements():
    return jsonify(populator.getMeasures())


@app.route("/api/submit", methods=["POST"])
def submit():
    myUtils.deleteAllFilesInDirectory()
    
    email = request.json.get("email")
    measure = request.json.get("measure")
    dateFrom = request.json.get("dateFrom")
    dateTo = request.json.get("dateTo")

    operation = request.json.get("operation")

    if measure is None or not all(item in populator.getMeasures() for item in measure):
        return Response("Sending 400 response, BAD_REQUEST", status=400)
    
    try:
        operationManager.set_current_operation(operation)
    except Exception as e:
        print(f"An Exception happend. Operation Not found! {type(e).__name__}")
        return Response("Sending 400 response, NO_OP", status=400)

    if operationManager.get_current_operation_Thread() and operationManager.get_current_operation_Thread().getBusyFlag():
        return Response("Sending 400 response, BUSY", status=400)
    
    if dateFrom is None or dateTo is None:
        return Response("Sending 400 response, INVALID_DATE", status=400)
    
    date_tuple = (dateFrom,dateTo)
    operationManager.set_date_tuple(date_tuple)
    operationManager.set_end_user_email(email)
    operationManager.set_tables(measure)

    print(f"submit func => Operation Start")
    fileManager.set_totalNumber(len(measure))
    fileManager.set_current_file(None)
    # start operation
    operationManager.startOperation()
    print(f"operation {operationManager.get_current_operation_name()} started")
    return Response("Sending 200 response", status=200)

@app.route('/api/list_files', methods=["GET"])
def list_files():
    file_list = myUtils.listCsvFilesInDirectory()
    return jsonify(file_list)

@app.route('/api/download/<filename>')
def download_file(filename):
    return send_from_directory(targetDirectory, filename)

@app.route('/api/deleteAll')
def deleteAll():
    res = myUtils.deleteAllFilesInDirectory()
    if not res:
        return Response("Sending 200 response", status=200)
    return Response("Sending 400 response, BAD_REQUEST", status=400)

@app.route('/api/delete/<filename>')
def delete_csv_file(filename):
    res = myUtils.deleteOneFileInDirectory(filename)
    if res:
        return Response("Sending 200 response", status=200)
    return Response("Sending 400 response, BAD_REQUEST", status=400)

@app.route('/api/doexit')
def do_force_exit():
    stop_threads()
    return Response("Sending Good and Comfy Byes ╭∩╮ʕ•ᴥ•ʔ╭∩╮", status=200)


def stop_threads():
    if operationManager.get_current_operation_Thread() is not None: 
        operationManager.halt_and_gracefully_kill()
        print("Stopping threads...")
    else:
        print("Current Thread Non no need to kill")
   

if __name__ == "__main__":
    atexit.register(stop_threads)
    app.run(host="0.0.0.0", port="8080", debug=False)
    sys.exit()
    
