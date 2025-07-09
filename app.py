import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    return '''
        <h1>You're home now!</h1>
        <p><a href="/hello-world">Go to Hello World</a></p>
    '''

@app.route('/hello-world')
def hello_world():
    return '''
        <p style="font-size:24px; color:blue;">Hello World</p>
        <p><a href="/">Back to Home</a></p>
    '''
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
