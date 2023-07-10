from exts import db
from datetime import datetime


class UserModel(db.Model):

    __tablename__ = "user"

    # 表的字段,及字段类型，id主键， autoincrement自动增长 id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # varchar null =0 nullable 表示字段不能为空
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)  # 唯一性
    join_time = db.Column(db.DateTime, default=datetime.now)   # 时间DateTime类型，这里是第一次进入后，调用这个函数，不是拿这个值


class EmailCaptchaModel(db.Model):

    __tablename__ = "email_captcha"
    # 创建邮箱表，2个字段， email 和captcha
    # 表的字段,及字段类型，id主键， autoincrement自动增长 id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # varchar null =0 nullable 表示字段不能为空
    email = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)
