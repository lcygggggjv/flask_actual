import random
import string
from flask import url_for    # 加载静态文件方法，包括url
from flask import redirect    # 重新跳到对应页面方法
from flask import Blueprint, render_template, jsonify, session
# FLASK 的子模块
from exts import mail, db
from flask_mail import Message
from flask import request
from models import EmailCaptchaModel
from .forms import RegisterForm, LoginForm   # 从当前forms文件里导入一个Registerform的方法
from models import UserModel
from werkzeug.security import generate_password_hash, check_password_hash    # 1 加密密码方法  2 校验 参数1加密密码和 2明文密码是否正确

# 参数蓝图名称 ,__name__当前文件  url_prefix 登录前缀
bp = Blueprint("author", __name__, url_prefix="/author")


# 登录前缀 /author/login
@bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'GET':
        return render_template("login.html")

    else:
        form = LoginForm(request.form)
        # 验证表单数据是否正确 ⬇
        if form.validate():
            email = form.email.data
            password = form.password.data
            # 查找数据库 邮箱和密码
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库里不存在")
                return redirect(url_for("author.login"))
            # 再对比数据库密码对不对，user.password加密密码
            if check_password_hash(user.password, password):
                # cookie不适合存储太多数据，只存储少量数据，只存放登录授权的东西
                # flask中session，经过加密存储cookie里 类似字典
                # 存储user)id到数据库里，登录生成了cookie，session经过加密，放到cookie里，传给浏览器，浏览器存储下来，浏览器访问其他页面
                # ，发送给服务器，服务器拿到cookie 解密 拿到userid用户id就知道
                session['user_id'] = user.id
                return redirect('/')

            else:
                print("密码错误！")
                return redirect(url_for("author.login"))
        else:
            print(form.errors)
            return redirect(url_for("author.login"))   # 登录失败还返回登录页面


@bp.route('/mail/test')
def mail_test():
    # 实例邮箱对象 ，传入内容，账号 通过mail.send_message发送 subject标题， recipients可以多个 body内容
    message = Message(subject="邮箱测试", recipients=['1721124043@qq.com'], body="测试邮件")
    mail.send(message)   # 直接用send方法发送！ 不是send_message

    return "邮件发送成功！"


# 默认get请求，提交数据用post
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # 输入的时候，不输入带入层级，直接写对应的名称就好
    if request.method == 'GET':
        return render_template("register.html")
    else:
        # 验证用户提交邮箱和验证码是否正确
        # 表单验证 flask-wtf；wtforms
        form = RegisterForm(request.form)   # 类对象实例，传入request
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))  # 加密方法
            db.session.add(user)
            db.session.commit()
            # redirect('/author/login)  login等再蓝图里，所以需要author.包含里面
            return redirect(url_for("author.login"))   # 注册成功，跳转到登录页面

        else:
            print(form.errors)
            # 注册失败还返回注册页面
            return redirect(url_for("author.register"))


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
