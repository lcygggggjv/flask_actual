from flask import Blueprint

# 蓝图名称 __name__当前文件  前缀
bp = Blueprint("qa", __name__, url_prefix="/")


# 前缀 回答页面，在根路径，不需要前缀 直接访问http://127.0.0.1:5000
@bp.route('/')
def index():

    return "首页展示！"
