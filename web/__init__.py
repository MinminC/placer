from flask import Flask
from config import appcfgs

app = Flask(__name__)
app.config.from_object(appcfgs.Config)

from web.main import controller
