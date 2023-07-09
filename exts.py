# flask-sqlalchemy  插件存放地方
# 解决循环引用问题

from flask_sqlalchemy import SQLAlchemy

# 先不传入app对象  在app文件里导入绑定
db = SQLAlchemy()
