from application import app
from flask_sqlalchemy import SQLAlchemy
import pymssql
from config import db_config

app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pymssql://" + db_config.DB_USER + ":" + db_config.DB_PASS + "@" + db_config.DB_SERV + "/" + db_config.DB_NAME
db = SQLAlchemy(app)
