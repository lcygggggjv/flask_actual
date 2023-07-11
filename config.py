

SECRET_KEY = "AYDHEHJEYEWHJR"

# mysql所在主机名
HOSTNAME = "127.0.0.1"

# MYSQL监听的端口号，默认3306
PORT = 3306

# 连接mysql的用户名，读者自己设置
USERNAME = "root"

# 连接mysql的密码，读者自己设置
PASSWORD = "123456789"

# 连接mysql数据库的名称
DATABASE = "questions_answers"

DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI = DB_URI


# hysfvorhtwymhgcd邮件码 第三方邮箱
# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "1743998121@qq.com"
MAIL_PASSWORD = "hysfvorhtwymhgcd"
MAIL_DEFAULT_SENDER = "1743998121@qq.com"
