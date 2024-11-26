from flask import Flask

from app.db.config import DbSettings
from app.config import ENV_FILE_PATH
from app.db.database import Database


app = Flask(__name__)
db_settings = DbSettings(_env_file=ENV_FILE_PATH)
db = Database(db_settings)
