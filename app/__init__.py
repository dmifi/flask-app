from flask import Flask
from app import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_CONNECTION_URI
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)



from app import routes, models
