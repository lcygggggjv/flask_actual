from exts import db
from datetime import datetime


class UserModel(db.Model):

    __tablename__ = "user"

    # 表的字段,及字段类型，id主键， autoincrement自动增长 id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # varchar null =0 nullable 表示字段不能为空
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(300), nullable=False)
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


class QuestionModel(db.Model):

    __tablename__ = "question"
    # 创建问答表，3个字段， 标题title 和内容content，创建时间 和一个外键user_id
    # 表的字段,及字段类型，id主键， autoincrement自动增长 id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # varchar null =0 nullable 表示字段不能为空
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    # 外键 表示用的是user表里的id字段
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # relationship反向引用， 引用user模型。通过拿到user的所有问答问题
    author = db.relationship(UserModel, backref='questions')

    # 创建完orm模型，映射到数据库


class AnswerModel(db.Model):

    __tablename__ = "answer"
    # 创建回答表，2个字段， 内容 和创建时间
    # 表的字段,及字段类型，id主键， autoincrement自动增长 id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    # 外键 拿到对应的键
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # 关系 反向引用 排序按照创建时间倒序
    question = db.relationship(QuestionModel, backref=db.backref('answers', order_by=create_time.desc()))
    author = db.relationship(UserModel, backref='answers')
