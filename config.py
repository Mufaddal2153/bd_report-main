import os
from flask import Flask

bd_report = Flask(__name__)
bd_report.config['SECRET_KEY'] = 'MyKey'

basedir = os.path.abspath(os.path.dirname(__file__))
