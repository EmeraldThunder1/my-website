from flask import Flask, render_template, make_response, request, url_for, jsonify
from datetime import datetime, timedelta
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cookies/', methods=['GET', 'POST'])
def cookies():
    if request.method == 'POST':
        with open('data/cookies.json') as f:
            data = json.load(f)
            f.close()

        cookie_string = ''
        for _cookie in data['cookies']:
            cookie_string += str(int(True if request.form.get(_cookie['name']) == 'on' else False))

        print(cookie_string)
        
        response = make_response(render_template('index.html'))

        
        if cookie_string[0] == '1':
            response.set_cookie('consent', cookie_string, expires=datetime.now() + timedelta(days=14))

        for i in range(len(cookie_string)):
            if cookie_string[i] == '0':
                response.delete_cookie(data['cookies'][i]['name'])

        response.headers['location'] = url_for('index')


        return response, 302


    with open('data/cookies.json') as f:
        data = json.load(f)
        f.close()

    return render_template('cookies.html', cookies=data['cookies'])

@app.route('/api/cookies/')
def api_cookies():
    with open('data/cookies.json') as f:
        data = json.load(f)
        f.close()

    return jsonify(data)

app.run('localhost')