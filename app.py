from config import *

from controllers.user_controller import *
from controllers.schedule_controller import *
from controllers.film_controller import *

db.create_all()


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/api/v1/hello-world-16')
def start():
    return 'Hello World 16'


if __name__ == '__main__':
    app.run()
