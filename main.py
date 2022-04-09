from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cookies/')
def cookies():
    return render_template('cookies.html')

app.run('localhost')