# InfluxDB Data Exporter

The InfluxDB Data Exporter is a Flask-based web application that connects to the InfluxDB API, allowing users to query selected measurements, and provides the ability to download data in CSV format directly in the browser. Additionally, users can receive the selected measurements via email in 7zip format.

# Tale of Contents
- [Dockerization](#dockerization)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Dockerization<a name="Dockerization"></a>
Simply Run `docker build -t backup-tool-webserver .` for building the image.
Run `docker run -d --name backup-tool-container -p 8000:8080 backup-tool-webserver`
Web server should be running on port 8080

## Installation Without Docker <a name="installation"></a>

Instructions for installing the project.
run `pip install -r requirements.txt`

Specify the port you want to run the webserver on. I used gunicorn for production WSGI server. 
Line below runs gunicorn server with 4 workers, binding to specified IP_ADDRESS:PORT
run `gunicorn -w 4 -b 0.0.0.0:8080 app:app`

In case you do not want to use gunicorn for as webserver, use the project in standalone mode.
run `python app.py`

## Usage <a name="usage"></a>

Instructions for using the project.

## Configuration <a name="configuration"></a>

The influxdb client and mail server credentials are located Dockerfile environmental variables.
The measures are located in tables.txt, this file can be dynamically changed based on what measures were configured when CSV file was compiled.


## Contributing <a name="contributing"></a>

The project was written in html and vanilla JS which for the purpose of the project are more than capable.
However the frontend can be replaced by any other framework or front end UI library which are more aesthetically pleasing.

Backend is written in Python (Flask) and is complete as is.
