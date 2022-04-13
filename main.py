from flask import Flask, render_template, make_response, request, url_for, jsonify
from datetime import datetime, timedelta
import json
import os
import markdown
import re

app = Flask(__name__)

class Post:
    def __init__(self, title, content, date, url, sample, read_time, author):
        self.title = title
        self.content = content
        self.date = date
        self.url = url
        self.sample = sample
        self.read_time = read_time
        self.author = author

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
    # TODO: Rework entire post system

    files = os.listdir(blogPath)
    posts = []

    for file in files:

        md = markdown.Markdown(extensions=['meta'])

        with open(blogPath + file) as f:
            content = f.read()
            content = md.convert(content)
            f.close()

        name = md.Meta['title'][0]

        date = os.path.getmtime(blogPath + file)
        date = datetime.fromtimestamp(date)

        author = md.Meta['author'][0]

        no_tags = re.sub(r'<.*?>', '', content)
        sample = no_tags[:100] + '...'

        read_time = round(len(no_tags) / 200)

        posts.append(Post(name, content, date, file.split('.')[0], sample, read_time, author))

    return posts

@app.route('/blog/')
def blog():
    return render_template('blog.html', posts=getPosts())

@app.route('/blog/post/<post_name>/')
def post(post_name):
    posts = getPosts()
    
    render_post = None
    for post in posts:
        if post.url == post_name:
            render_post = post
            break

    if render_post == None:
        return '404 this is a placeholder'

    return render_template('post.html', post=render_post)

@app.route('/api/blog/posts/')
def api_blog_posts():
    return jsonify(getPosts())

@app.route('/api/blog/posts/<post_id>/')
def api_post_id(post_id):
    print(type(getPosts()))
    return jsonify(getPosts()['posts'][int(post_id)])

app.run('localhost')