from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from watchlist import app, db
from watchlist.models import User, Movie


@app.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] # html页面中input元素的name属性
        password = request.form['password']

        if not username or not password:
            flash("Invalid Input")
            return redirect(url_for('login'))

        user = User.query.first()
        if username==user.username and user.validate_password(password):
            login_user(user)
            flash('Login successfully!')
            return redirect(url_for('index'))

        flash('You are wrong,game is over.')
        return redirect(url_for('login'))

    return render_template('login.html')
    # 此处必须返回页面，如果写了下面这一句，那么就会没完没了的重定向
    # return redirect(url_for('login'))

@app.route('/logout')
@login_required # 用于视图保护
def logout():
    logout_user() # 登出用户
    flash('You are log out')
    # return render_template('login.html')
    # 此处不能直接返回页面，因为必须改变地址栏的地址，否则后续无法登陆
    return redirect(url_for('index'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))

        current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))

    return render_template('settings.html')


@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index')) # 重定向到主页
        title_now = request.form.get('title')
        year_now = request.form.get('year')
        if not title_now or not year_now or len(year_now)>4 or len(title_now)>60:
            flash('Invalid input')
            return redirect(url_for('index'))
        movie_now = Movie(title = title_now,year = year_now)
        db.session.add(movie_now)
        db.session.commit()
        flash('Bingo!')
        return redirect(url_for('index'))


    # user = User.query.first() # 读取用户记录
    movies = Movie.query.all() # 读取用户记录
    return render_template('index.html',movies=movies)


@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']

        if not title or not year or len(year)!=4 or len(title)>60:
            flash('Invalid input')
            return redirect(url_for('edit',movie_id=movie_id))
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Edit Successfully!')
        return redirect(url_for('index'))

    return render_template('edit.html',movie=movie)



@app.route('/movie/delete/<int:movie_id>',methods=['POST'])
@login_required # 登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('You delete it successfully')
    return redirect(url_for('index'))

