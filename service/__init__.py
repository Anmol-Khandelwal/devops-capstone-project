import os
from flask import Flask
from flask_talisman import Talisman
from flask_cors import CORS
from service.models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URI", "sqlite:///test.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

talisman = Talisman(app, force_https=False)
cors = CORS(app)

from service import routes  # noqa: E402, F401

with app.app_context():
    db.create_all()

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")
app.logger.info("Service initialized!")
