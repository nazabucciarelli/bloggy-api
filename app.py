from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import ForeignKey

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:@localhost/bloggy_db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(20), nullable=False)

    def __str__(self) -> str:
        return self.username


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False) 

    def __str__(self) -> str:
        return self.name 


class Post(db.Model):
    __tablename__ = "post"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(300), nullable=False)
    date = db.Column(db.Date, nullable=False)
    edit_date = db.Column(db.Date, nullable=True)

    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    category_id = db.Column(db.Integer, ForeignKey(
        "category.id"), nullable=False)

    def __str__(self) -> str:
        return self.title


class Commentary(db.Model):
    __tablename__ = "commentary"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    edit_date = db.Column(db.Date, nullable=True)
    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    post_id = db.Column(db.Integer, ForeignKey("post.id"), nullable=False)

    def __str__(self) -> str:
        return self.content


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register") 
def register():
    return render_template("register.html")

@app.route("/post", methods=['POST'])
def post():
    pass  