from datetime import datetime
from flask_login import logout_user, current_user
from flask_admin.contrib.sqla import ModelView
from flask import redirect, request
from flask_admin import BaseView, expose, Admin, AdminIndexView
from wtforms import TextAreaField
from wtforms.widgets import TextArea
from app import db, app, dao
from app.models import Category, Product, User, UserRoleEnum, Tag, MedicalBill


class AuthenticatedModelView(ModelView):
    def is_accessible(self):  # Nếu đăng nhập quyền ADMIN mới hiển thị View
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.ADMIN

class AuthenticatedDOCTORModelView(ModelView):
    def is_accessible(self):  # Nếu đăng nhập quyền DOCTOR mới hiển thị View
        return current_user.is_authenticated and current_user.user_role == UserRoleEnum.DOCTOR

class AuthencatedBaseView(BaseView):
    def is_accessible(self): #Nếu đăng nhập mới hiển thị View
        return current_user.is_authenticated

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
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)

        return self.render('admin/states.html',
                           month=dao.stats_by_month(year=year),
                           stats=dao.stats_revenue(kw=kw,
                                                     from_date=from_date,
                                                     to_date=to_date))

class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        month = request.args.get('month', datetime.now().month)
        stats = dao.count_user_by_day(month=month)
        return self.render('admin/index.html', stats=stats)


admin = Admin(app=app, name='SAIGONIZ.COM', template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(AuthenticatedModelView(Category, db.session, name='Categories'))
admin.add_view(ProductModelView(Product, db.session,name='Products'))
admin.add_view(AuthenticatedModelView(User, db.session,name='Users'))
admin.add_view(AuthenticatedModelView(Tag, db.session, name='Tag'))
admin.add_view(AuthenticatedDOCTORModelView(MedicalBill, db.session, name='Medical Bill'))
admin.add_view(StatsView(name='Report'))
admin.add_view(LogoutView(name='Log Out'))



