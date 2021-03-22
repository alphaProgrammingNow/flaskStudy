from flask import render_template
from watchlist import app

# 使用 app.errorhandler() 装饰器注册一个错误处理函数
@app.errorhandler(404) # 传入要处理的错误代码
def page_not_found(e): # 接受异常对象作为参数
    # user = User.query.first()
    return render_template('errors/404.html'),404  # 返回模板和状态码
# 普通的视图函数之所以不用写出状态码，是因为默认会使用 200 状态码，表示成功


@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('errors/500.html'), 500




