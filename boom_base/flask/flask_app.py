from flask_cors import CORS
import os
from flask import Flask

app = Flask(__name__)


if os.environ.get('is_production', False):
    CORS(app, supports_credentials=True)

CORS_INSTANCE = CORS()
CORS_INSTANCE.init_app(app=app, resources={r"*": {"origins": "*"}})

