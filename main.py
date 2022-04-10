from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cookies/', methods=['GET', 'POST'])
def cookies():
    with open('data/cookies.json') as f:
        data = json.load(f)
        f.close()

    return render_template('cookies.html', cookies=data['cookies'])

app.run('localhost')