import os
from flask import Flask
from flask_mysqldb import MySQL


bd_report = Flask(__name__)
bd_report.config['SECRET_KEY'] = 'MyKey'


mysql=MySQL(bd_report)
bd_report.config['MYSQL_HOST'] = '192.168.10.4'
bd_report.config['MYSQL_USER'] = 'admin'
bd_report.config['MYSQL_PASSWORD'] = 'Admin!123'
bd_report.config['MYSQL_DB'] = 'bd_report'
bd_report.config['MYSQL_PORT'] = 3307


basedir = os.path.abspath(os.path.dirname(__file__))