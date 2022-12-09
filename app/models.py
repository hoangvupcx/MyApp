from sqlalchemy import Column, Integer, Boolean, Float, String, Text, ForeignKey, Enum, DateTime
from sqlalchemy.orm import relationship, backref
from app import app, db
from enum import Enum as UserEnum
from flask_login import UserMixin
from datetime import datetime

class UserRoleEnum(UserEnum):
    USER = 1
    ADMIN = 2
    DOCTOR = 3
class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    email = Column(String(50))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    user_role = Column(Enum(UserRoleEnum), default=UserRoleEnum.USER)
    active = Column(Boolean, default=True)
    receipts = relationship('Receipt', backref='user', lazy=True)
    medicalBill = relationship('MedicalBill', backref='user', lazy=True)
    report = relationship('Report', backref='user', lazy=True)
    #comments = relationship('Comment', backref='user', lazy=True)



    def __str__(self):
        return self.name


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=False)

    def __str__(self): # Overriding, lấy tên đối tượng của Category
        return self.name # self = this (java/C#)

class Tag(BaseModel):
    name = Column(String(50), nullable=False, unique=True)

    def __str__(self):
        return self.name


prod_tag = db.Table('prod_tag',
                    Column('product_id', Integer,
                           ForeignKey('product.id'), nullable=False, primary_key=True),
                    Column('tag', Integer,
                           ForeignKey('tag.id'), nullable=False, primary_key=True))



class Product(BaseModel):
    __tablename__ = 'product'

    name = Column(String(50), nullable=False)
    description = Column(Text)
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    tags = relationship('Tag', secondary='prod_tag',
                        lazy='subquery',
                        backref=backref('products', lazy=True))
    receipt_details = relationship('ReceiptDetails', backref='product', lazy=True)
    products = relationship('MedicalBill', secondary='prod_medibill',
                            lazy='subquery',
                            backref=backref('products', lazy=True))
    #comments = relationship('Comment', backref='products', lazy=True)

    def __str__(self):
        return self.name


prod_medibill = db.Table('prod_medibill',
                         Column('product_id', Integer,
                                ForeignKey('product.id'), nullable=False, primary_key=True),
                         Column('medicalbill', Integer,
                                ForeignKey('medical_bill.id'), nullable=False, primary_key=True))


class MedicalBill(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    fee = Column(Integer, default=100000)
    guide = Column(String(100))
    symptom = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)





class MedicalBilLDetails():
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)


class Report(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='reprot', lazy=True)
    receipt = relationship('Receipt', backref='reprot', lazy=True)
class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetails', backref='receipt', lazy=True)
    report_id = Column(Integer, ForeignKey(Report.id))



class ReceiptDetails(BaseModel):
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    report_id = Column(Integer, ForeignKey(Report.id))

# class Comment(BaseModel):
#     content = Column(String(255), nullable=False)
#     created_date = Column(DateTime, default=datetime.now())
#     product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
#     user_id = Column(Integer, ForeignKey(User.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()


