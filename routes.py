from flask import Flask, render_template, request
from werkzeug.exceptions import BadRequest
from flask_sqlalchemy import SQLAlchemy
import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://localhost/learningflask'
app.debug = True
db = SQLAlchemy(app)

class Blog(db.Model):
    __tablename__='blogs'
    bid=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(200))
    author = db.Column(db.String(100))
    date= db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)
    content=db.Column(db.String(200000))

class Myblog(db.Model):
    __tablename__='myblogoverview'
    mbid=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200))
    author=db.Column(db.String(200))
    overview=db.Column(db.String(10000))
    coverimage=db.Column(db.String(1000))
    date=db.Column(db.TIMESTAMP,default=datetime.datetime.utcnow)

class Expertblog(db.Model):
    __tablename__='expertblogoverview'
    ebid=db.Column(db.Integer,primary_key=True)
    topic=db.Column(db.String(200))
    subtitle=db.Column(db.String(500))
    coverimage=db.Column(db.String(500))
    author=db.Column(db.String(1000))

class Eblogcontent(db.Model):
    __tablename__='eblogcontent'
    cid=db.Column(db.Integer,primary_key=True)
    articleid=db.Column(db.Integer)
    content=db.Column(db.String(100000))

class Myblogcontent(db.Model):
    __tablename__='mblogcontent'
    cid=db.Column(db.Integer,primary_key=True)
    articleid=db.Column(db.Integer)
    content=db.Column(db.String(100000))

    

# @app.route('/')
# def index():
#     return render_template("index.html")

@app.route('/')
def home():
    myblog_data=Myblog.query.order_by(Myblog.mbid.desc()).limit(3)
    expertblog_data=Expertblog.query.all()
    return render_template('home.html', myblog_data=myblog_data,expertblog_data=expertblog_data)

@app.route('/content')
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

