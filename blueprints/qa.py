from flask import Blueprint, render_template, request, g, redirect, url_for
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel
from exts import db
from decorators import login_required


# 蓝图名称 __name__当前文件  前缀
bp = Blueprint("qa", __name__, url_prefix="/")


# 前缀 回答页面，在根路径，不需要前缀 直接访问http://127.0.0.1:5000
@bp.route('/')
def index():
    # 获取所有的问答,按照创建时间倒序排序
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()

    return render_template('index.html', questions=questions)


@bp.route('/qa/public', methods=['GET', 'POST'])
@login_required     # 运用装饰器函数先判断有没有登录
def public_question():
    # 首页， 判断是否是get请求，返回首页模板
    if request.method == 'GET':

        return render_template('public_question.html')
    else:
        form = QuestionForm(request.form)
        # 如果验证成功
        if form.validate():
            title = form.title.data
            content = form.content.data
            # 存储到数据库里
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            # 跳转到问答详情页
            return redirect('/')
        else:
            print(form.errors)
            # 否则跳转到问答页面
            return redirect(url_for('qa.public_question'))


@bp.route('/qa/detail/<qa_id>')
def qa_detail(qa_id):
    # 传入qa_id <variable>表示变量
    question = QuestionModel.query.get(qa_id)
    # 把question传给模板里 id
    return render_template('detail.html', question=question)


# @bp.route('/answer/public', methods=['POST'])
@bp.post('/answer/public')
@login_required
def public_answer():
    # 表单验证
    form = AnswerForm(request.form)
    # 验证成功，通过
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()

        # 重定向页面 表单验证成功，直接用question_id 反转要那个写到对应qa文件
        return redirect(url_for('qa.qa_detail', qa_id=question_id))
    else:
        print(form.errors)
        # 失败就获取，表单request.form里的id 能够取到
        return redirect(url_for('qa.qa_detail', qa_id=request.form.get('question_id')))


@bp.route('/search')
def search():
    # 查询字符串方式  、/search?q=flask  获取参数
    # /search/<q>  传参数
    # post ,request.form, 通过表单接口获取
    q = request.args.get('q')       # 通过接口参数，获取q
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()  # 查询标题包含q关键词的数据返回给 questions
    return render_template('index.html', questions=questions)


"""
url 传参
邮件发送
aiax 发请求
orm模型 与数据库
Jinja2 模板
cookie 和session原理处理

search 搜索
"""


