
from flask import Flask
import config
from exts import db, mail

from models import UserModel
# 导入定义蓝图
from blueprints.questions_answers import bp as qa_bp
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


# 绑定蓝图
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)


# blueprint  模块化
# 蓝图，插件，等


@app.route('/')
def hello():
    # 首页
    return "hello word"


if __name__ == '__main__':

    app.run(debug=True)
