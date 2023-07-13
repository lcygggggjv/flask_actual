
from flask import Flask, session, g
import config
from exts import db, mail

from models import UserModel
# 导入定义蓝图
from blueprints.qa import bp as qa_bp
from blueprints.author import bp as auth_bp
# 映射数据创建字段等
from flask_migrate import Migrate


app = Flask(__name__)

# 绑定配置文件
app.config.from_object(config)

# 初始化绑定app导入
db.init_app(app)
mail.init_app(app)

# 映射数据库创建字段
migrate = Migrate(app, db)

# flask db init 初始化执行一次
# flask db migrate 将orm模型生成迁移脚本
# flask db upgrade 将迁移脚本映射到数据库里，如果开始设置数据库字段var=100，后面改成200，需要到数据库手动修改


# 绑定蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)


# blueprint  模块化
# 蓝图，插件，等


# before_request / before_first_request / after_request  钩子函数 类似前置函数操作， 登录前先校验一下
@app.before_request
def my_before_request():
    # 导入session，获取里面的user_id，不需要解密，自己解密了
    user_id = session.get('user_id')
    # 不登陆，，没有cookie，没有session 就是none
    # 如果有user)id，再查
    if user_id:
        user = UserModel.query.get(user_id)
        # 导入全局变量g globals,通过setattr  g 里，设置一个user属性，值就是获取到的user
        setattr(g, "user", user)
    else:
        # 不存在user，也设置，user属性，值是none，不会报错
        setattr(g, "user", None)


# 上下文处理器，上下文变量对象，模板渲染都会传进去
@app.context_processor
def my_context_processor():

    # 返回上面获取的g，user对象，所有模板都能使用
    return {"user": g.user}


@app.route('/')
def hello():
    # 首页
    return "hello word"


if __name__ == '__main__':

    app.run(debug=True)
