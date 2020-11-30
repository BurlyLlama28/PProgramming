from flask import Flask
from wsgiref.simple_server import make_server
from flask_sqlalchemy import SQLAlchemy
from repository.models import Base
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = URL = os.getenv("URL")
db = SQLAlchemy(app)
db.Model = Base


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/api/v1/hello-world-16')
def start():
    return 'Hello World 16'


def run():
    with make_server('', 5000, app) as server:
        print("Super? MAYBE:]")

        server.serve_forever()

if __name__ == '__main__':
    run()

