from marshmallow import fields
from app import ma

# User schemas


class UserBasicSchema(ma.Schema):
    username = fields.String()


class UserPrivateSchema(UserBasicSchema):
    password = fields.String()


class UserSchema(UserBasicSchema):
    id = fields.Integer(dump_only=True)
    visible = fields.Boolean()

# Post schemas


class PostEditSchema(ma.Schema):
    title = fields.String()
    content = fields.String()


class PostBasicSchema(PostEditSchema):
    user_id = fields.Integer()
    category_id = fields.Integer()


class PostSchema(PostBasicSchema):
    id = fields.Integer(dump_only=True)
    date = fields.Date()
    edit_date = fields.Date()
    visible = fields.Boolean()

# Commentary schemas


class CommentaryEditSchema(ma.Schema):
    content = fields.String()


class CommentaryBasicSchema(CommentaryEditSchema):
    user_id = fields.Integer()
    post_id = fields.Integer()


class CommentarySchema(CommentaryBasicSchema):
    id = fields.Integer(dump_only=True)
    date = fields.Date()
    edit_date = fields.Date()
    visible = fields.Integer()

# Category schemas


class CategoryBasicSchema(ma.Schema):
    name = fields.String()


class CategorySchema(CategoryBasicSchema):
    id = fields.Integer(dump_only=True)
    visible = fields.Integer()
