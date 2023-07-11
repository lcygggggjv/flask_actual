import wtforms
from wtforms.validators import Email, Length, EqualTo   # 表单校验
from models import UserModel, EmailCaptchaModel
from exts import db


# 表单form 验证前端提交数据是否符合要求 继承FORM方法不是小写的
class RegisterForm(wtforms.Form):

    # 验证错误提示
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    # 校验验证码格式，长度是否正确
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！")])
    # 校验用户格式
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    # 确认密码，和上面的密码相同，是断言相同的
    password_confirm = wtforms.StringField(validators=[EqualTo("password", message="两次密码不一致！")])

    # 自定义验证码：
    # 邮箱是否被注册
    # 验证码是否正确
    """
    函数里定义的filed，就是对应的 .data获取字段的值
    """
    def validate_email(self, field):

        email = field.data
        user = UserModel.query.filter_by(email=email).first()

        if user:
            raise wtforms.ValidationError(message="改邮箱已经被注册！")

    # 验证码是否正确  验证对应，field就是验证码
    def validata_captcha(self, field):

        captcha = field.data

        email = self.email.data

        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).fiest()

        if not captcha_model:

            raise wtforms.ValidationError(message="邮箱或验证码错误！")

            # #  to do ：可以定期删掉
        # else:
        #     db.session.deleta(captcha_model)
        #     db.session.commit()


class LoginForm(wtforms.Form):

    # 验证错误提示
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
