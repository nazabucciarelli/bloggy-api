from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func


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
    date = db.Column(DateTime(timezone=True),
                     server_default=func.now(), nullable=False)
    edit_date = db.Column(DateTime(timezone=True),
                          onupdate=func.now(), nullable=True)

    user_id = db.Column(db.Integer, ForeignKey("user.id"), nullable=False)
    category_id = db.Column(db.Integer, ForeignKey(
        "category.id"), nullable=False)

    def __str__(self) -> str:
        return self.title


class Commentary(db.Model):
    __tablename__ = "commentary"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date = db.Column(DateTime(timezone=True),
                     server_default=func.now(), nullable=False)
    edit_date = db.Column(DateTime(timezone=True),
                          onupdate=func.now(), nullable=True)
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
    post_title = request.form['title']
    post_content = request.form['content']
    post_user_id = request.form['user']
    post_category_id = 1
    post_date = func.current_timestamp()
    post_edit_date = None
    new_post = Post(title=post_title, content=post_content, date=post_date, edit_date=post_edit_date,
                    user_id=post_user_id, category_id=post_category_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('index'))


@app.route("/comment/<post_id>", methods=['POST'])
def comment(post_id):
    comment_content = request.form['comment_content']
    comment_date = func.current_timestamp()
    comment_edit_date = None
    comment_user_id = request.form['comment_user_id']
    new_comment = Commentary(content=comment_content, date=comment_date,
                             edit_date=comment_edit_date, user_id=comment_user_id, post_id = post_id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('index'))


@app.context_processor
def inject_posts():
    posts = db.session.query(Post).all()
    return dict(posts=posts)


@app.context_processor
def inject_users():
    users = db.session.query(User).all()
    return dict(users=users)


@app.context_processor
def inject_comments():
    comments = db.session.query(Commentary).all()
    return dict(comments=comments)


@app.context_processor
def inject_categories():
    categories = db.session.query(Category).all()
    return dict(categories=categories)
