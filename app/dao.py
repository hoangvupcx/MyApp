from app.models import Category, Product, User, Receipt, ReceiptDetails #, Comment
from app import db
import hashlib
from flask_login import current_user
from sqlalchemy import func, extract


def load_categories():
    return Category.query.all()



# Push products from SQL
def load_products(category_id=None, kw=None):
    query = Product.query.filter(Product.active.__eq__(True))

    if category_id:
        query = query.filter(Product.category_id.__eq__(category_id))
    # if from_price:
    #     query = query.filter(Product.category_id.__ge__(from_price))
    # if to_price:
    #     query = query.filter(Product.category_id.__le__(to_price))
    if kw:
        query = query.filter(Product.name.contains(kw))
    return query.all()


def get_product_by_id(product_id):
    return Product.query.get(product_id)


def get_user_by_id(user_id):
    return User.query.get(user_id)



# Proceed to uodate all products (consist who currently logged, quantity, price, id of product) - in models.py
def add_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)

        for c in cart.values():
            detail = ReceiptDetails(quantity=c['quantity'], price=c['price'], receipt=receipt, product_id=int(c['id']))
            db.session.add(detail)
        try:
            db.session.commit()
        except:
            return False
        else:
            return True



# Hash password and check password match to register password yet?
def check_login(username, password):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password)).first()



# Create acoount and compare password to confirm (1 account consists: name, username, password and avatar)
def register(name, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name,username=username,password=password,avatar=avatar)
    db.session.add(u)
    db.session.commit()



# Field in report: View categories and quantity with each category
def count_product_by_cate():
    return db.session.query(Category.id, Category.name, func.count(Product.id))\
        .join(Product, Product.category_id.__eq__(Category.id), isouter=True)\
        .group_by(Category.id).order_by(Category.id).all()



# Field in report: total users in one day (which day) by month
def count_user_by_day(month):
    return db.session.query(extract('day',Receipt.created_date), func.count(User.id))\
                    .join(User, Receipt.user_id.__eq__(User.id)) \
                    .filter(extract('month', Receipt.created_date) == month)\
                    .group_by(extract('day', Receipt.created_date)) \
                    .order_by(extract('day', Receipt.created_date)) \
                    .all()



# Filed in report: Stats for products' id, products, categories, quantities,
#                  times (total how many times this product was created),
#                  total revenue. Can researched (filtered) by key-word, from and to date
def stats_revenue(kw=None, from_date=None, to_date=None):
     query = db.session.query(Product.id, Product.name, Product.category_id ,func.sum(ReceiptDetails.quantity),
                              func.count(ReceiptDetails.quantity), func.sum(ReceiptDetails.quantity * ReceiptDetails.price))\
                       .join(ReceiptDetails, ReceiptDetails.product_id.__eq__(Product.id))\
                       .join(Receipt, ReceiptDetails.receipt_id.__eq__(Receipt.id)) \
                       .group_by(Product.id, Product.name).order_by(Product.id)
     if kw:
         query = query.filter(Product.name.contains(kw))

     if from_date:
         query = query.filter(Receipt.created_date.__ge__(from_date))

     if to_date:
         query = query.filter(Receipt.created_date.__le__(to_date))

     return query.group_by(Product.id).order_by(Product.name).all()


# Filed in report: View with total revenue in a month and
#                  how many percent in subtotal.
#                  Can filtered by Year (Show all months have receipts and revenue)
def stats_by_month(year):
    a = db.session.query(func.sum(ReceiptDetails.quantity * ReceiptDetails.price))
    return db.session.query(extract('month', Receipt.created_date),
                            func.sum(ReceiptDetails.quantity * ReceiptDetails.price),
                            100 * (func.sum(ReceiptDetails.quantity * ReceiptDetails.price) / func.avg(a)))\
                     .join(ReceiptDetails, ReceiptDetails.receipt_id.__eq__(Receipt.id))\
                     .filter(extract('year', Receipt.created_date) == year)\
                     .group_by(extract('month', Receipt.created_date))\
                     .order_by(extract('month', Receipt.created_date))\
                     .all()

# def load_comments_by_prod(product_id):
#     return Comment.query.filter(Comment.product_id.__eq__(product_id)).order_by(-Comment.id).all()


# def add_comment(product_id, content):
#     c = Comment(content=content, product_id=product_id, user=current_user)
#     db.session.add(c)
#     db.session.commit()
#
#     return c


if __name__ == '__main__':
    from app import app
    # with app.app_context():
        # print(load_comments_by_prod(1))