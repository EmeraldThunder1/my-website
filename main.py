from flask import Flask, render_template, make_response, request, url_for, jsonify
from datetime import datetime, timedelta
import json
import os
import markdown

app = Flask(__name__)

blogPath = './data/posts/'

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

def getPosts():
    files = os.listdir(blogPath)
    posts = []

    for file in files:
        fileName = file.split('.')[0].replace('-', ' ')

        with open(blogPath + file) as f:
            content = f.read()
            content = markdown.markdown(content)
            f.close()

        date = os.path.getmtime(blogPath + file)
        date = datetime.fromtimestamp(date)
        date = f'{date.day}/{date.month}/{date.year}'

        posts.append({'title': fileName, "content": content, "date": date})

    return {"posts": posts}

@app.route('/blog/')
def blog():
    return render_template('blog.html', posts=getPosts()['posts'])

@app.route('/blog/post/<post_id>/')
def post(post_id):
    return render_template('post.html', posts=getPosts()['posts'][post_id])

@app.route('/api/blog/posts/')
def api_blog_posts():
    return jsonify(getPosts())

@app.route('/api/blog/posts/<post_id>/')
def api_post_id(post_id):
    print(type(getPosts()))
    return jsonify(getPosts()['posts'][int(post_id)])

app.run('localhost')