from app import admin, db, app
from app.models import Category, Product, User, UserRoleEnum
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, Admin
from flask_login import logout_user, current_user
from flask import redirect
from wtforms import TextAreaField
from wtforms.widgets import TextArea

class AuthenticatedModelView(ModelView):
    def is_accessible(self):  # Nếu đăng nhập quyền admin mới hiển thị View
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN




class CKTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' ckeditor'
        else:
            kwargs.setdefault('class', 'ckeditor')
        return super(CKTextAreaWidget, self).__call__(field, **kwargs)

class CKTextAreaField(TextAreaField):
    widget = CKTextAreaWidget()


class ProductModelView(AuthenticatedModelView):
    column_filters = ['name', 'price']
    column_searchable_list = ['name', 'description']
    column_exclude_list = ['image']
    can_view_details = True
    can_export = True
    column_labels = {
        'name': 'Name',
        'price': 'Price',
        'description': 'Description'
    }
    form_overrides = {
        'description': CKTextAreaField
    }
    extra_js = ['//cdn.ckeditor.com/4.6.0/standard/ckeditor.js']
    page_size = 10


class AuthencatedBaseView(BaseView):
    def is_accessible(self): #Nếu đăng nhập mới hiển thị View
        return current_user.is_authenticated


class LogoutView(AuthencatedBaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')



class StatsView(AuthencatedBaseView):
    @expose('/')
    def index(self):
        return self.render('admin/states.html')






#admin = Admin(app=app, name="Quản trị bán hàng", templatemode='bootstrap4')
admin.add_view(AuthenticatedModelView(Category, db.session, name='Categories'))
admin.add_view(ProductModelView(Product, db.session,name='Products'))
admin.add_view(AuthenticatedModelView(User, db.session,name='Users'))
admin.add_view(StatsView(name='Report'))
admin.add_view(LogoutView(name='Log Out'))



