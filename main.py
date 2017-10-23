from flask import Flask, render_template, request
from werkzeug.exceptions import BadRequest
from flask.ext.cache import Cache
import datetime
import os
import mysql.connector

# https://wildchildyn@childrenasd.scm.azurewebsites.net/childrenasd.git   (azure git)

app = Flask(__name__)
app.debug = True
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

db = mysql.connector.connect(host='childrenasd.mysql.database.azure.com',database='childrenasd',user='wildchildyn@childrenasd',password='abcd1234!')

class Myblog:
    def __init__(self, mbid, title, author, overview, coverimage):
        self.mbid = mbid
        self.title = title
        self.author = author
        self.overview = overview
        self.coverimage = coverimage

class Expertblog:
    def __init__(self, ebid, topic, subtitle, coverimage, author):
        self.ebid = ebid
        self.topic = topic
        self.subtitle = subtitle
        self.coverimage = coverimage
        self.author = author

class Eblogcontent:
    def __init__(self, cid, articleid, content):
        self.cid = cid
        self.articleid = articleid
        self.content = content

class Myblogcontent:
    def __init__(self, cid, articleid, content):
        self.cid = cid
        self.articleid = articleid
        self.content = content
    
# @app.route('/')
# def index():
#     return render_template("index.html")

@app.route('/')
@cache.cached(timeout=10)
def home():
    cur = db.cursor()
    cur.execute("SELECT ebid,topic,subtitle,coverimage,author from expertblogoverview;")
    expertblog_data = []
    for row in cur.fetchall():
        expertblog_data.append(Expertblog(row[0], row[1], row[2], row[3], row[4]))

    myblog_data = []
    #myblog_data=Myblog.query.order_by(Myblog.mbid.desc()).limit(10)
    return render_template('home.html', myblog_data=myblog_data,expertblog_data=expertblog_data)

@app.route('/content')
#@cache.cached(timeout=10)
def content():
    bid=request.args.get('bid')
    btype=request.args.get('type')
    if btype=='expert':
        bcontent_data=Eblogcontent.query.filter(Eblogcontent.articleid==bid).one()
        btitle_data=Expertblog.query.filter(Expertblog.ebid==bid).one()
        return render_template('content.html',bcontent_data=bcontent_data,btitle_data=btitle_data)
    elif btype=='my':
        bcontent_data=Myblogcontent.query.filter(Myblogcontent.articleid==bid).one()
        btitle_data=Myblog.query.filter(Myblog.mbid==bid).one()
        return render_template('content.html',bcontent_data=bcontent_data,btitle_data=btitle_data)
    else:
        raise BadRequest()
    
@app.route('/addblog')
def addblogs():
    return render_template("addblog.html")

@app.route('/post_blog',methods=['POST'])
def post_blog():
    blog=Blog()
    blog.title=request.form['titlename']
    blog.author=request.form['authorname']
    blog.content=request.form['contentname']
    db.session.add(blog)
    db.session.commit()
    return 'success'

@app.route('/abc')
def layout():
    blogs_data = Blog.query.all()
    return render_template("layout.html", xxx=blogs_data, yyy=blogs_data)

@app.route('/about2')
def about1():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()
