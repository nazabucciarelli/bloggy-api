# Imports de frameworks y libs
from flask import ( 
    request, 
    jsonify)

from sqlalchemy.sql import func
from flask.views import MethodView

# Imports generados por nosotros
from app import app, db
from app.schemas.schemas import (
    UserBasicSchema, 
    UserSchema,
    UserPrivateSchema,
    CategorySchema,
    CommentarySchema,
    PostSchema,
    PostBasicSchema,
    PostEditSchema,
    CategoryBasicSchema,
    CommentaryBasicSchema,
    CommentaryEditSchema)
from app.models.models import (
    User,
    Category,
    Post,
    Commentary
)

@app.route("/")
def index():
    return "Welcome to the Bloggy API!"

class UserAPI(MethodView):
    def get(self,user_id=None):
        if user_id is None:
            users = User.query.all()
            users_schema = UserSchema().dump(users,many=True)
            return jsonify(users_schema)
        user = User.query.get(user_id)
        return jsonify(UserBasicSchema().dump(user))

    def post(self):
        user_json = UserPrivateSchema().load(request.json)
        username = user_json.get('username')
        password = user_json.get('password')
        new_user =  User(username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(UserSchema().dump(new_user))

    def put(self,user_id):
        user = User.query.get(user_id)
        user_json = UserPrivateSchema().load(request.json)
        username = user_json.get("username")
        password = user_json.get("password")
        user.username = username
        user.password = password
        db.session.commit()
        return jsonify(UserSchema().dump(user))

    def delete(self,user_id):
        user = User.query.get(user_id)
        user.visible = 0
        db.session.commit()
        return jsonify(UserSchema().dump(user))

class CategoryAPI(MethodView):
    def get(self,category_id=None):
        if category_id is None:
            categories = Category.query.all()
            categories_schema = CategorySchema().dump(categories,many=True)
            return jsonify(categories_schema)
        category = Category.query.get(category_id)
        return jsonify(CategorySchema().dump(category))

    def post(self):
        category_json = CategoryBasicSchema().load(request.json)
        name = category_json.get('name')
        new_category =  Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return jsonify(CategorySchema().dump(new_category))

    def put(self,category_id):
        category = Category.query.get(category_id)
        category_json = CategoryBasicSchema().load(request.json)
        name = category_json.get('name')
        category.name = name
        db.session.commit()
        return jsonify(CategorySchema().dump(category))

    def delete(self,category_id):
        category = Category.query.get(category_id)
        category.visible = 0
        db.session.commit()
        return jsonify(CategorySchema().dump(category))
    
class PostAPI(MethodView):
    def get(self, post_id=None):
        if post_id is None:
            posts = Post.query.all()
            posts_schema = PostSchema().dump(posts,many=True)
            return jsonify(posts_schema)
        post = Post.query.get(post_id)
        post_schema = PostSchema().dump(post)
        return jsonify(post_schema)

    def post(self):
        post_json = PostBasicSchema().load(request.json)
        title = post_json.get('title')
        content = post_json.get('content')
        user_id = post_json.get('user_id')
        category_id = post_json.get('category_id')
        visible = post_json.get('visible')
        new_post =  Post(title=title,content=content,user_id=user_id,
                         category_id=category_id,visible=visible)
        db.session.add(new_post)
        db.session.commit()
        return jsonify(PostSchema().dump(new_post))

    def put(self,post_id):
        post = Post.query.get(post_id)
        post_json = PostEditSchema().load(request.json)
        title = post_json.get('title')
        content = post_json.get('content')
        post.title = title
        post.content = content
        db.session.commit()
        return jsonify(PostSchema().dump(post))

    def delete(self,post_id):
        post = Post.query.get(post_id)
        post.visible = 0
        db.session.commit()
        return jsonify(PostSchema().dump(post))

class CommentaryAPI(MethodView):
    def get(self, commentary_id=None):
        if commentary_id is None:
            commentaries = Commentary.query.all()
            commentaries_schema = CommentarySchema().dump(commentaries,many=True)
            return jsonify(commentaries_schema)
        commentary = Commentary.query.get(commentary_id)
        commentary_schema = CommentarySchema().dump(commentary)
        return jsonify(commentary_schema)

    def post(self):
        commentary_json = CommentaryBasicSchema().load(request.json)
        content = commentary_json.get('content')
        user_id = commentary_json.get('user_id')
        post_id = commentary_json.get('post_id')
        new_commentary =  Commentary(content=content,user_id=user_id,
                                     post_id=post_id)
        db.session.add(new_commentary)
        db.session.commit()
        return jsonify(CommentarySchema().dump(new_commentary))

    def put(self,commentary_id):
        commentary = Commentary.query.get(commentary_id)
        commentary_json = CommentaryEditSchema().load(request.json)
        content = commentary_json.get('content')
        commentary.content = content
        db.session.commit()
        return jsonify(CommentarySchema().dump(commentary))

    def delete(self,commentary_id):
        commentary = Commentary.query.get(commentary_id)
        commentary.visible = 0
        db.session.commit()
        return jsonify(CommentarySchema().dump(commentary))

app.add_url_rule("/user",view_func=UserAPI.as_view('user'))
app.add_url_rule("/user/<user_id>",view_func=UserAPI.as_view('user_id'))

app.add_url_rule("/category",view_func=CategoryAPI.as_view('category'))
app.add_url_rule("/category/<category_id>",view_func=CategoryAPI.
                 as_view('category_id'))

app.add_url_rule("/post",view_func=PostAPI.as_view('post'))
app.add_url_rule("/post/<post_id>",view_func=PostAPI.as_view('post_id'))

app.add_url_rule("/commentary",view_func=CommentaryAPI.as_view('commentary'))
app.add_url_rule("/commentary/<commentary_id>",view_func=CommentaryAPI.
                 as_view('commentary_id'))