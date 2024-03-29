from flask import session
from app import app, login, utils, controllers, dao, admin
from app import *


app.add_url_rule('/', 'index', controllers.index)
app.add_url_rule('/products/<int:product_id>', 'product-detail', controllers.product_detail)
app.add_url_rule('/login', 'login-user', controllers.login_my_user, methods=['get', 'post'])
app.add_url_rule('/logout', 'logout', controllers.logout_my_user)
app.add_url_rule('/login-admin', 'login-admin', controllers.admin_login, methods=['post'])
app.add_url_rule('/register', 'register', controllers.register, methods=['get', 'post'])
app.add_url_rule('/cart', 'cart', controllers.cart)
app.add_url_rule('/cart', 'add-cart', controllers.add_to_cart, methods=['post'])
app.add_url_rule('/cart/<product_id>', 'update-cart', controllers.update_cart, methods=['put'])
app.add_url_rule('/cart/<product_id>', 'delete-cart', controllers.delete_cart, methods=['delete'])
app.add_url_rule('/delete', 'delete-all', controllers.delete_all)
app.add_url_rule('/pay', 'pay', controllers.pay, methods=['post'])
app.add_url_rule('/book', 'book', controllers.booking_page)
# app.add_url_rule('/products/<product_id>/comments', 'comments', controllers.comments)
# app.add_url_rule('/products/<product_id>/comments', 'comment-add', controllers.add_comment, methods=['post'])


# Get data from SQl
@app.context_processor
def common_data():
    categories = dao.load_categories()
    return {
        'categories': categories,
        'cart': utils.cart_stats(session.get(app.config['CART_KEY']))
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id=user_id)


if __name__ == '__main__':
    app.run(debug=True)