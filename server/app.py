from flask import Flask
from os import path

app = Flask(__name__)

@app.route('/upload')
def upload():
    with open(path.join('static', 'raw-data', 'CDH_tm_processed.txt')) as f:
        print(f.readline())

    return "Hello"

if __name__ == '__main__':
    app.run(debug=True)
    # upload()