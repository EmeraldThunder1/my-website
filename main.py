from flask import Flask, render_template, make_response, request, url_for, jsonify
from datetime import datetime, timedelta
import json
import os
import markdown
import re
import requests

app = Flask(__name__)


class Post:
    def __init__(self, title, content, date, url, sample, read_time, author, tags):
        self.title = title
        self.content = content
        self.date = date
        self.url = url
        self.sample = sample
        self.read_time = read_time
        self.author = author
        self.tags = tags


class Software:
    def __init__(self, name, description, icon, fileUrl):
        self.fileUrl = fileUrl
        self.name = name
        self.description = description
        self.url = self.getUrl()
        self.icon = icon
        self.repoName = self.getRepo()

    def getUrl(self):
        return self.name.lower().replace(" ", "-")

    def getRepo(self):
        return '/'.join(self.fileUrl.split("/")[-2: -1])


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
            cookie_string += str(
                int(True if request.form.get(_cookie['name']) == 'on' else False))

        print(cookie_string)

        response = make_response(render_template('index.html'))

        if cookie_string[0] == '1':
            response.set_cookie('consent', cookie_string,
                                expires=datetime.now() + timedelta(days=14))

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


def getSoftware():
    with open('data/software.json') as f:
        data = json.load(f)
        f.close()
    software = []
    for item in data['software']:
        software.append(Software(item['name'], item['description'], item['icon'], item['url']))

    return software


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

        tags = md.Meta['tags']

        author = md.Meta['author'][0]

        no_tags = re.sub(r'<.*?>', '', content)
        sample = no_tags[:100] + '...'

        read_time = round(len(no_tags) / 200)

        posts.append(Post(name, content, date, file.split('.')
                     [0], sample, read_time, author, tags))

    return posts


@app.route('/blog/', methods=['GET', 'POST'])
def blog():
    if request.method == 'POST':
        search = request.form.get('search')

        all_posts = getPosts()
        posts = []

        for post in all_posts:
            if search.lower() in post.tags:
                posts.append(post)

                continue

            if search.lower() in post.title.lower():
                posts.append(post)

                continue

            if search.lower() in post.content.lower():
                posts.append(post)

                continue

        return render_template('blog.html', posts=posts)

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


@app.route('/software/', methods=['GET', 'POST'])
def software():

    if request.method == 'POST':
        search = request.form.get('search')

        software = getSoftware()
        software_list = []

        for item in software:
            if search.lower() in item.name.lower():
                software_list.append(item)

                continue

            if search.lower() in item.description.lower():
                software_list.append(item)

                continue

        return render_template('software.html', software=software_list)
        
    return render_template('software.html', software=getSoftware())

@app.route('/software/<download_name>/')
def download(download_name):
    software = getSoftware()

    download = None
    for item in software:
        if item.url == download_name:
            download = item
            break

    if download == None:
        return '404 this is a placeholder'

    return render_template('download.html', software=download)


app.run('localhost')
