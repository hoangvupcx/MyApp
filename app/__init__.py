from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_babelex import Babel
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)

app.secret_key = 'jnkjnadba98wq9@21431&9097' # Dùng để mã hóa khi thêm/sửa/xóa/cập nhât dữ liệu dưới quyền Admin
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/test1?charset=utf8mb4' % quote('Admin@123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)
admin = Admin(app=app, name='SAIGONIZ.COM', template_mode='bootstrap4')
login = LoginManager(app=app)
babel = Babel(app=app)
# @babel.localeselector
# def load_locale():
#     return 'vi'

cloudinary.config(cloud_name='dbk4i3dvv', api_key='378148229852699', api_secret='Fpn0QT24PEvDsODPUKMjE_S8s8M')



