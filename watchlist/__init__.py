import sys
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'




app = Flask(__name__)
# os.getenv('SECRET_KEY', 'dev') 表示读取系统环境变量 SECRET_KEY 的值，如果没有获取到，则使用 dev
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
# 注意更新这里的路径，把 app.root_path 添加到 os.path.dirname() 中
# 以便把文件定位到项目根目录
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path),os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# 除了实例化扩展类之外，我们还要实现一个“用户加载回调函数”
@login_manager.user_loader
def load_user(user_id): # 创建用户加载回调函数，接受用户 ID 作为参数
    from watchlist.models import User
    user = User.query.get(int(user_id)) # 用 ID 作为 User 模型的主键查询对应的用户
    return user # 返回用户对象
    
 
 
# 未登录用户访问delete等页面时，我们不能让他访问，我们要让他重定向，重定向到哪里？就在这里决定
# 登录视图端点（函数名）
login_manager.login_view='login'



@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)
# 这个函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文环境中，因此可以直接在模板中使用。


from watchlist import views,errors,commands






















