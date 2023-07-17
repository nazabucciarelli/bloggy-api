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
    visible = db.Column(db.Boolean, default=True, nullable=False)

    def __str__(self) -> str:
        return self.username


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    visible = db.Column(db.Boolean, default=True, nullable=False)

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
    visible = db.Column(db.Boolean, default=True, nullable=False)

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
    visible = db.Column(db.Boolean, default=True, nullable=False)

    def __str__(self) -> str:
        return self.content


@app.route("/")
def index():
    return render_template("welcome.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/modal_edit")
def modal_edit():
    return render_template("modal_edit.html")


@app.route("/post/<category_id>", methods=['POST'])
def post(category_id):
    post_title = request.form['title']
    post_content = request.form['content']
    post_user_id = request.form['user']
    post_category_id = category_id
    post_date = func.current_timestamp()
    post_edit_date = None
    new_post = Post(title=post_title, content=post_content, date=post_date, edit_date=post_edit_date,
                    user_id=post_user_id, category_id=post_category_id, visible=1)
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('inject_posts', category_id=post_category_id))


@app.route("/comment/<post_id>", methods=['POST'])
def comment(post_id):
    comment_content = request.form['comment_content']
    comment_date = func.current_timestamp()
    comment_edit_date = None
    comment_user_id = request.form['comment_user_id']
    new_comment = Commentary(content=comment_content, date=comment_date,
                             edit_date=comment_edit_date, user_id=comment_user_id, post_id=post_id, visible=1)
    db.session.add(new_comment)
    db.session.commit()
    category_id = db.session.query(Post).get(post_id).category_id
    return redirect(url_for('inject_posts', category_id=category_id))


@app.route("/get_posts/<category_id>")
def inject_posts(category_id):
    posts = db.session.query(Post).filter(Post.category_id == category_id)
    posts_count = posts.filter(Post.visible == 1).count()
    return render_template('index.html', posts=posts, category_id=int(category_id), posts_count=posts_count)


@app.route("/register_user", methods=['POST'])
def register_user():
    register_username = request.form['username']
    register_password = request.form['password']
    register_email = request.form['email']
    success = False
    username_exists = db.session.query(User).filter(
        User.username == register_username).count() > 0
    if not username_exists:
        new_user = User(email=register_email,
                        username=register_username, password=register_password, visible=1)
        db.session.add(new_user)
        db.session.commit()
        success = True
    return render_template('register.html', success=success)


@app.route("/login_user", methods=['POST'])
def login_user():
    login_username = request.form['username']
    login_password = request.form['password']
    success = False
    user = db.session.query(User).filter(
        User.username == login_username).first()
    try:
        if user.password == login_password:
            success = True
    except:
        pass
    return render_template('login.html', success=success)


@app.route("/edit_post/<post_id>", methods=['POST'])
def edit_post(post_id):
    post = db.session.query(Post).get(post_id)    
    post.title = request.form[f'new_title_post{post_id}']
    post.content = request.form[f'new_content_post{post_id}']
    post.edit_date = func.current_timestamp()
    db.session.commit()
    return inject_posts(post.category_id)

@app.route("/edit_comment/<comment_id>", methods=['POST'])
def edit_comment(comment_id):
    comment = db.session.query(Commentary).get(comment_id)    
    comment.content = request.form[f'new_content_comment{comment_id}']
    comment.edit_date = func.current_timestamp()
    post = db.session.query(Post).get(comment.post_id)
    db.session.commit()
    return inject_posts(post.category_id)

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


@app.route("/delete_post/<post_id>", methods=['POST'])
def delete_post(post_id):
    post = db.session.query(Post).get(post_id)
    post.visible = 0
    db.session.commit()
    return inject_posts(post.category_id)


@app.route("/delete_comment/<comment_id>", methods=['POST'])
def delete_comment(comment_id):
    comment = db.session.query(Commentary).filter(
        Commentary.id == comment_id).first()
    comment.visible = 0
    post = db.session.query(Post).filter(Post.id == comment.post_id).first()
    db.session.commit()
    return inject_posts(post.category_id)
