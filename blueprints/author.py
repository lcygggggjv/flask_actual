from flask import Blueprint, render_template
# FLASK 的子模块


# 参数蓝图名称 ,__name__当前文件  url_prefix 登录前缀
bp = Blueprint("author", __name__, url_prefix="/author")


# 登录前缀 /author/login
@bp.route('/login')
def login():

    return "登录成功！"


@bp.route('/register')
def register():
    # 输入的时候，不输入带入层级，直接写对应的名称就好
    return render_template("register.html")
