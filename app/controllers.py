from flask import render_template, request, jsonify, session, redirect  # redirect: Chuyển sang trang mới hoàn toàn nếu đăng nhập thành công
from app import app, login, utils, dao
from flask_login import login_user, logout_user, login_required
from app.decorators import annonymous_user
from app.admin import *
import cloudinary.uploader



# Filter products by category_id or key-word
def index():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    # from_price = request.args.get('from_price')
    # to_price = request.args.get('to_price')
    products = dao.load_products(category_id=cate_id, kw=kw)
    return render_template('index.html',
                           products=products)


#
def common_data():
    categories = dao.load_categories()
    return {
        'categories': categories,
        'cart': utils.cart_stats(session.get(app.config['CART_KEY']))
    }


def product_detail(product_id):
    p = dao.get_product_by_id(product_id)
    return render_template('details.html', product=p)




@annonymous_user
def login_my_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = dao.check_login(username=username, password=password)
        if user:
            login_user(user=user)

            u = request.args.get('next')
            return redirect(u if u else '/') # To continue the previous page after log-in (cart.html)

    return render_template('/login.html')


def logout_my_user():
    logout_user()
    return render_template('/login.html')


def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = dao.check_login(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)


def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']

        if password.__eq__(confirm):  # compare password and confirm
            # upload avatar to cloudinary
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['avatar'])
                avatar = res['secure_url']

            # save user
            try:
                dao.register(name=request.form['name'], username=request.form['username'], password=request.form['password'], avatar=avatar)

                return redirect('/login')
            except:
                err_msg = "UPDATING, COMING SOON!"
        else:
            err_msg = "NOT MATCH PASSWORD!"
    return render_template('register.html', err_msg=err_msg)


def cart():
    return render_template('cart.html')



# Take product_id, quantity, price, name, image(detail cart) and add to cart
def add_to_cart():
    data = request.json
    id = str(data['id'])

    key = app.config['CART_KEY']
    cart = session[key] if key in session else {}

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        name = data['name']
        price = data['price']
        image = str(data['image'])

        cart[id] = {
            "id": id,
            "image": image,
            "name": name,
            "price": price,
            "quantity": 1
        }
    session[key] = cart
    return jsonify(utils.cart_stats(cart))



# When customers want to change product's quantity
def update_cart(product_id):
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart and product_id in cart:
        quantity = int(request.json['quantity'])
        cart[product_id]['quantity'] = quantity
    session[key] = cart
    return jsonify(utils.cart_stats(cart))


# To take product away from cart or when customers completely check-out
def delete_cart(product_id):
    key = app.config['CART_KEY']
    cart = session.get(key)

    if cart and product_id in cart:
        del cart[product_id]

    session[key] = cart
    return jsonify(utils.cart_stats(cart))


# Log-in is an optional and when complete payment, all products in cart will be remove
@login_required
def pay():
    if 'cart' in session and session['cart']:
        dao.add_receipt(cart=session['cart'])
        del session['cart']

        return jsonify({'message': 'Successful'})
    return jsonify({'message': 'Failed'})

# To remove all the products in cart
def delete_all():
    if 'cart' in session and session['cart']:
        del session['cart']

        return jsonify({'message': 'Successful'})
    return jsonify({'message': 'Failed'})


def booking_page():
    return render_template('booking.html')


# def comments(product_id):
#     data = [] # serializer
#     for c in dao.load_comments_by_prod(product_id):
#         data.append({
#             "id": c.id,
#             "content": c.content,
#             "created_date": str(c.created_date),
#             "user": {
#                 "name": c.user.name,
#                 "avatar": c.user.avatar
#             }
#         })
#
#     return jsonify(data)


# def add_comment(product_id):
#     try:
#         c = dao.add_comment(product_id, request.json['content'])
#     except:
#         return jsonify({'status': 500})
#     else:
#         return jsonify({
#             'status': 204,
#             'comment': {
#                 "id": c.id,
#                 "content": c.content,
#                 "created_date": str(c.created_date),
#                     "user": {
#                         "name": c.user.name,
#                         "avatar": c.user.avatar
#                     }
#             }
#         })


if __name__ == '__main__':
    app.run(debug=True)
