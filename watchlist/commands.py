import click

from watchlist import app,db
from watchlist.models import User,Movie

@app.cli.command()
@click.option('--drop',is_flag=True,help='Create after drop')
def initdb(drop):
    """Initialize the database"""
    if drop: # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialize database.') #输出提示信息


@app.cli.command()
def forge():
    """Generate fake data"""
    # 如果没有db.drop_all(),那么,就在数据库原有的两张表的基础上，继续添加记录
    db.create_all()
    name = 'alpha2'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
        {'title': 'Harry Potter', 'year': '2012'},
        {'title': '我和我的家乡', 'year': '2020'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')



@app.cli.command()#注册为命令
@click.option('--userName',prompt=True,help='login user name')
@click.option('--password',prompt=True,hide_input=True,confirmation_prompt=True,help='login user password')
def admin(username,password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('更新用户名...')
        user.username = username
        user.set_password(password)

    else:
        click.echo('创建新用户...')
        user = User(username=username,name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')