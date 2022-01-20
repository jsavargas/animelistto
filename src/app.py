import time


from flask import Flask
from routes.index import index


app = Flask(__name__)


app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

app.register_blueprint(index)
