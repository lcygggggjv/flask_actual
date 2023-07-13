# 装饰器判断是否登录
from functools import wraps
from flask import g, redirect, url_for


def login_required(func):

    # wraps保留原来函数的信息
    @wraps(func)
    def inner(*args, **kwargs):
        # 判断有没有登录。 获取g的user有没有值。有值表示登录了，
        if g.user:
            # 有的话正常执行这个函数
            return func(*args, **kwargs)
        else:
            # 没有登录就到跳转登录页面
            return redirect(url_for("author.login"))
    # 最后返回整个函数的
    return inner


"""
@login_required
def public_question(question_id):
    pass
等于  
login_required(public_question)(question_id)

"""
