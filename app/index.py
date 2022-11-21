from flask import render_template, request, redirect # redirect: Chuyển sang trang mới hoàn toàn nếu đăng nhập thành công
from app import app, login
from flask_login import login_user, logout_user
import dao
import os
from app.admin import *
import cloudinary.uploader


@app.route('/')
def index():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    # from_price = request.args.get('from_price')
    # to_price = request.args.get('to_price')
    products = dao.load_products(category_id=cate_id, kw=kw)
    return render_template('index.html',
                           products=products)

@app.context_processor #Lấy dữ liệu từ SQL
def common_data():
    categories = dao.load_categories()
    return {
        'categories': categories
    }

@app.route('/products/<int:product_id>')
def product_detail(product_id) :
    p = dao.get_product_by_id(product_id)
    return render_template('details.html', product=p)


@app.route('/login', methods=['post', 'get'])
def login_my_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.check_login(username=username, password=password)
        if user:
            login_user(user=user)
            return redirect('/')

    return render_template('login.html')




@app.route('/logout')
def logout_my_user():
    logout_user()
    return render_template('/login.html')

@app.route('/login-admin', methods=['post'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.check_login(username = username, password = password)
    if user:
        login_user(user=user)

    return redirect('/admin')

@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)

@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']

        if password.__eq__(confirm): # Kiểm tra xác nhận mật khẩu
            # upload avatar lên cloudinary
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            # save user
            try:
                dao.register(name=request.form['name'],
                             username=request.form['username'],
                             password=request.form['password'],
                             avatar=avatar)
                return redirect('/login')
            except:
                err_msg = "UPDATING, COMING SOON!"
        else:
            err_msg = "INCORRECT CONFIRM PASSWORD!"
    return render_template('register.html', err_msg=err_msg)



if __name__ == '__main__':
    app.run(debug=True)