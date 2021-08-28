from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "example.com"}})

import loanx.views