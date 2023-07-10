import random
import string

from flask import Blueprint, render_template, jsonify
# FLASK 的子模块
from exts import mail, db
from flask_mail import Message
from flask import request
from models import EmailCaptchaModel


# 参数蓝图名称 ,__name__当前文件  url_prefix 登录前缀
bp = Blueprint("author", __name__, url_prefix="/author")


# 登录前缀 /author/login
@bp.route('/login')
def login():

    return "登录成功！"


@bp.route('/mail/test')
def mail_test():
    # 实例邮箱对象 ，传入内容，账号 通过mail.send_message发送 subject标题， recipients可以多个 body内容
    message = Message(subject="邮箱测试", recipients=['1721124043@qq.com'], body="测试邮件")
    mail.send(message)   # 直接用send方法发送！ 不是send_message

    return "邮件发送成功！"


@bp.route('/register')
def register():
    # 输入的时候，不输入带入层级，直接写对应的名称就好
    return render_template("register.html")


# bp.route ;没有指定methods参数。默认就是get请求，
@bp.route('/captcha/email')
def get_email_captcha():
    #  uri路径传参  <email>是参数  /captcha/email/<email>
    # get url传参形式 /captcha/email?email=xx.qq.com
    email = request.args.get("email")    # 通过request》args参数意思 的get获取email参数
    # 随机产生验证码字母数字，组合
    # all_str = string.ascii_letters + string.digits
    # captcha = "".join(random.sample(all_str, 4))
    source = string.digits*4
    captcha = random.sample(source, 4)
    captcha = "".join(captcha)
    message = Message(subject="游戏人生注册验证码", recipients=[email], body=f"你的验证码是：{captcha}")
    mail.send(message)
    # 需要吧验证码存到数据库里，校验注册时对应的邮箱和验证码是否正确
    # 临时解决 ；用数据库表的方式存储 比较慢   # 必要还是用memcached/redis缓存 快
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    # 满足restful api格式
    # {code: 200/300/400. message: "",}
    return jsonify({"code": 200, "message": "", "data": None})


# def gets_co():
#
#     all_str = string.ascii_letters + string.digits
#     s_str = "".join(random.sample(all_str, 4))
#
#     return s_str
#
#
# if __name__ == '__main__':
#
#     ad = gets_co()
#     print(ad)
