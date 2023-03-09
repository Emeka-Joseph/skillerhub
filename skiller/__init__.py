from flask import Flask
#import mysql.connector as dt

from flask_sqlalchemy import SQLAlchemy 


from flask_wtf.csrf import CSRFProtect
#from skiller import config

app = Flask(__name__,instance_relative_config=True)
#csrf = CSRFProtect(app)

#load the config
app.config.from_pyfile('config.py', silent=False)

db = SQLAlchemy(app)
#load the routes

#datab = dt.connector.connect(database = 'skillerdb', user = 'root', password = '', host = 'localhost')
#mycursor = datab.cursor()

"""app = Flask(__name__)
mysql = MySQL(app)

app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]=""
app.config["MYSQL_DB"]="skillerdb"
app.config["MYSQL_cursorclass"]="DictCursor"""
 
 
from skiller import adminroutes,userroutes,forms