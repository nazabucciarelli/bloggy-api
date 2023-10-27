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
    def get(self, user_id=None):
        if user_id is None:
            users = User.query.all()
            users_schema = UserSchema().dump(users, many=True)
            return jsonify(users_schema), 200
        user = User.query.get(user_id)
        if user is None:
            msg = "User with that id doesn't exist."
            return jsonify(not_found=msg), 404
        return jsonify(UserBasicSchema().dump(user)), 200

    def post(self):
        try:
            user_json = UserPrivateSchema().load(request.json)
            username = user_json.get('username')
            password = user_json.get('password')
        except:
            msg = f"""The request must have username (str) 
              and password (str) fields."""
            return jsonify(request_error=msg), 400
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(UserSchema().dump(new_user)), 201

    def put(self, user_id):
        user = User.query.get(user_id)
        if user is None:
            msg = "User with that id doesn't exist."
            return jsonify(not_found=msg), 404
        try:
            user_json = UserPrivateSchema().load(request.json)
        except:
            msg = f"""The request must have username (str) and
              password (str) fields."""
            return jsonify(request_error=msg), 400
        username = user_json.get("username")
        password = user_json.get("password")
        user.username = username
        user.password = password
        db.session.commit()
        return jsonify(UserSchema().dump(user)), 200

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user is None:
            msg = "User with that id doesn't exist."
            return jsonify(not_found=msg), 404
        user.visible = 0
        db.session.commit()
        return jsonify(), 204


class CategoryAPI(MethodView):
    def get(self, category_id=None):
        if category_id is None:
            categories = Category.query.all()
            categories_schema = CategorySchema().dump(categories, many=True)
            return jsonify(categories_schema), 200
        category = Category.query.get(category_id)
        if category is None:
            msg = "Category with that id doesn't exist."
            return jsonify(not_found=msg), 404
        return jsonify(CategorySchema().dump(category)), 200

    def post(self):
        try:
            category_json = CategoryBasicSchema().load(request.json)
        except:
            msg = "The request must have name (str) field."
            return jsonify(request_error=msg), 400
        name = category_json.get('name')
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return jsonify(CategorySchema().dump(new_category)), 201

    def put(self, category_id):
        category = Category.query.get(category_id)
        if category is None:
            msg = "Category with that id doesn't exist."
            return jsonify(not_found=msg), 404
        try:
            category_json = CategoryBasicSchema().load(request.json)
        except:
            msg = "The request must have name (str) field."
            return jsonify(request_error=msg), 400
        name = category_json.get('name')
        category.name = name
        db.session.commit()
        return jsonify(CategorySchema().dump(category)), 200

    def delete(self, category_id):
        category = Category.query.get(category_id)
        if category is None:
            msg = "Category with that id doesn't exist."
            return jsonify(not_found=msg), 404
        category.visible = 0
        db.session.commit()
        return jsonify(), 204


class PostAPI(MethodView):
    def get(self, post_id=None):
        if post_id is None:
            posts = Post.query.all()
            posts_schema = PostSchema().dump(posts, many=True)
            return jsonify(posts_schema), 200
        post = Post.query.get(post_id)
        if post is None:
            msg = "Post with that id doesn't exist."
            return jsonify(not_found=msg), 404
        post_schema = PostSchema().dump(post)
        return jsonify(post_schema), 200

    def post(self):
        try:
            post_json = PostBasicSchema().load(request.json)
        except:
            msg = f"""The request must have title (str), content (str), user_id
                (int) and category_id (int) fields."""
            return jsonify(request_error=msg), 400
        title = post_json.get('title')
        content = post_json.get('content')
        user_id = post_json.get('user_id')
        category_id = post_json.get('category_id')
        new_post = Post(title=title, content=content, user_id=user_id,
                        category_id=category_id)
        db.session.add(new_post)
        db.session.commit()
        return jsonify(PostSchema().dump(new_post)), 201

    def put(self, post_id):
        post = Post.query.get(post_id)
        if post is None:
            msg = "Post with that id doesn't exist."
            return jsonify(not_found=msg), 404
        try:
            post_json = PostEditSchema().load(request.json)
        except:
            msg = "The request must have title (str) and content (str) fields."
            return jsonify(request_error=msg), 400
        title = post_json.get('title')
        content = post_json.get('content')
        post.title = title
        post.content = content
        db.session.commit()
        return jsonify(PostSchema().dump(post)), 200

    def delete(self, post_id):
        post = Post.query.get(post_id)
        if post is None:
            msg = "Post with that id doesn't exist."
            return jsonify(not_found=msg), 404
        post.visible = 0
        db.session.commit()
        return jsonify(), 204


class CommentaryAPI(MethodView):
    def get(self, commentary_id=None):
        if commentary_id is None:
            commentaries = Commentary.query.all()
            commentaries_schema = CommentarySchema().dump(commentaries,
                                                          many=True)
            return jsonify(commentaries_schema), 200
        commentary = Commentary.query.get(commentary_id)
        if commentary is None:
            msg = "Commentary with that id doesn't exist."
            return jsonify(not_found=msg), 404
        commentary_schema = CommentarySchema().dump(commentary)
        return jsonify(commentary_schema), 200

    def post(self):
        try:
            commentary_json = CommentaryBasicSchema().load(request.json)
        except:
            msg = """The request must have content (str), user_id (int)
              and post_id (int) fields."""
            return jsonify(request_error=msg), 400
        content = commentary_json.get('content')
        user_id = commentary_json.get('user_id')
        post_id = commentary_json.get('post_id')
        new_commentary = Commentary(content=content, user_id=user_id,
                                    post_id=post_id)
        db.session.add(new_commentary)
        db.session.commit()
        return jsonify(CommentarySchema().dump(new_commentary)), 201

    def put(self, commentary_id):
        commentary = Commentary.query.get(commentary_id)
        if commentary is None:
            msg = "Commentary with that id doesn't exist."
            return jsonify(not_found=msg), 404
        try:
            commentary_json = CommentaryEditSchema().load(request.json)
        except:
            msg = "The request must have content (str) field."
            return jsonify(request_error=msg), 400
        content = commentary_json.get('content')
        commentary.content = content
        db.session.commit()
        return jsonify(CommentarySchema().dump(commentary)), 200

    def delete(self, commentary_id):
        commentary = Commentary.query.get(commentary_id)
        if commentary is None:
            msg = "Commentary with that id doesn't exist."
            return jsonify(not_found=msg), 404
        commentary.visible = 0
        db.session.commit()
        return jsonify(), 204


app.add_url_rule("/user", view_func=UserAPI.as_view('user'))
app.add_url_rule("/user/<user_id>", view_func=UserAPI.as_view('user_id'))

app.add_url_rule("/category", view_func=CategoryAPI.as_view('category'))
app.add_url_rule("/category/<category_id>", view_func=CategoryAPI.
                 as_view('category_id'))

app.add_url_rule("/post", view_func=PostAPI.as_view('post'))
app.add_url_rule("/post/<post_id>", view_func=PostAPI.as_view('post_id'))

app.add_url_rule("/commentary", view_func=CommentaryAPI.as_view('commentary'))
app.add_url_rule("/commentary/<commentary_id>", view_func=CommentaryAPI.
                 as_view('commentary_id'))
