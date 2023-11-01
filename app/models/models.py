from app import db
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.sql import func


class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
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
    user = db.relationship('User')
    category_id = db.Column(db.Integer, ForeignKey(
        "category.id"), nullable=False)
    category = db.relationship('Category')
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
    user = db.relationship('User')
    post_id = db.Column(db.Integer, ForeignKey("post.id"), nullable=False)
    visible = db.Column(db.Boolean, default=True, nullable=False)

    def __str__(self) -> str:
        return self.content
