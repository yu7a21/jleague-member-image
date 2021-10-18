import os

from flask import Flask


app = Flask(__name__, instance_relative_config=True)
# a simple page that says hello
@app.route('/hello')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host="0.0.0.0")