from flask import Blueprint,render_template,redirect,url_for,request, flash
from .models import *
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])  
def home():
    products = Products.query.all()
    if request.method=='POST':
        search = request.form.get('search')
        products = Products.query.filter(Products.product_name.like(f'%{search}%')).all()
        return render_template('sadman.html', products=products)
    return render_template("sadman.html", products=products)

@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type') 
        print(email, password)
        if user_type.lower() == "admin":
            user = Admin.query.filter_by(email=email).first()
        if user_type.lower() == "customer":
            user = Customer.query.filter_by(email=email).first()
        if user:
            print("USER:",user)
            if check_password_hash(user.password, password):
                print("Logged in")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html")



@views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print(request.form)
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type').lower()
        if user_type.lower() == "admin":
            new_user = Admin(
                name = request.form.get('name'),
                email=email, 
                password=generate_password_hash(password, method='sha256'),
                user_type = 'admin',
                )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
        if user_type.lower() == "customer":
            new_user = Customer(
                nid = request.form.get('id'),
                name = request.form.get('name'),
                email=email, 
                password=generate_password_hash(password, method='sha256'),
                user_type = 'customer',
                )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("signup.html")

@views.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.login'))

@views.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if request.method == 'POST':
        print(request.form)
        product_amt = request.form.get('product_amt')
        product_name = request.form.get('product_name')
        product_description = request.form.get('product_desc')
        product_price = request.form.get('product_price')
        new_product = Products(
            product_amount=product_amt,
            product_name=product_name,
            product_description=product_description,
            product_price=product_price,
            )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template("addproduct.html")

@views.route('/removeproduct', methods=['GET', 'POST'])
def removeproduct():
    if request.method == 'POST':
        print(request.form)
        product_id = request.form.get('product_id')
        product = Products.query.filter_by(product_id=product_id).first()
        db.session.delete(product)
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template("deleteproduct.html")

@views.route('/makepayment', methods=['GET', 'POST'])
def makepayment():
    if request.method == 'POST':
        print(request.form)
        amt = request.form.get('payamt')
        user = Customer.query.filter_by(email=current_user.email).first()
        if user is None:
            user = Admin.query.filter_by(email=current_user.email).first()
        
        user.balance = user.balance + int(amt)
        db.session.commit()
        return redirect(url_for('views.home'))
    return render_template("payment.html")

@views.route('/cart', methods=['POST', 'GET'])
def cart():
    # if request.method=='POST':
    product = Products.query.first()
    cart = Cart(product=product.product_id)
    db.session.add(cart)
    db.session.commit()
    return render_template('cart.html', product=product)

@views.route('/headphone', methods=['POST', 'GET'])
def headphone():
    products = Products.query.filter(Products.product_name.like('%headphone%')).all()
    return render_template('sadman.html', products=products)

@views.route('/monitor', methods=['POST', 'GET'])
def monitor():
    products = Products.query.filter(Products.product_name.like('%monitor%')).all()
    return render_template('sadman.html', products=products)

@views.route('/mouse', methods=['POST', 'GET'])
def mouse():
    products = Products.query.filter(Products.product_name.like('%mouse%')).all()
    return render_template('sadman.html', products=products)

@views.route('/keyboard', methods=['POST', 'GET'])
def keyboard():
    products = Products.query.filter(Products.product_name.like('%keyboard%')).all()
    return render_template('sadman.html', products=products)
