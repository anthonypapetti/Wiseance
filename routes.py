from run import app, db
from flask import render_template, session, redirect, request, jsonify
from forms import LoginForm, RegisterForm, AddAmazonForm, DeleteAmazonForm
from models import User, Product
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required, get_ASIN, get_amzn_data
import requests
from bs4 import BeautifulSoup
import decimal

decimal.getcontext().prec = 2

@app.route("/")
def index():
    if session.get("user_id"):
        return render_template("landing.html")
    else:
        return render_template("layout.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        session["user_id"] = user.id
    return render_template("login.html", form=form)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password = generate_password_hash(request.form["password"])
        user = User(username=request.form["username"],password= password)
        db.session.add(user)
        db.session.commit()
        session["user_id"] = user.id
        return redirect("/")
    return render_template("register.html", form=form)

@app.route("/wishlist", methods=["POST", "GET"])
@login_required
def wishlist():
    form = AddAmazonForm()
    if form.is_submitted():
        if form.validate_on_submit():
            #get simplified amazon link
            link = "https://www.amazon.com/"
            extension = get_ASIN(form.amazonlink.data)
            extension = extension.group(0)
            link = link + extension

            #scrape price and product title from page
            productdata = get_amzn_data(link)
            
            #converts price into decimal
            #takes the first of any $xprice - $yprice listings and gets rid of the $
            productdata["regprice"] = productdata["regprice"].split('-')[0].strip("$")
            print(productdata["regprice"])

            #add product to database
            product = Product(user_id=session["user_id"], title=productdata["title"], price=decimal.Decimal(productdata["regprice"]))
            db.session.add(product)
            db.session.commit()
    
    #get data to display in table
    data = Product.query.filter_by(user_id=session["user_id"]).all()
    print(data)

    return render_template("amazon.html", form=form, data=data)


@app.route("/deleteamazon", methods=["GET"])
@login_required
def deleteamazon():
    title = request.args.get("name")
    title = title.strip()
    print(title)
    data = Product.query.filter_by(title=title).first()
    print(data)
    if not data:
        return jsonify(False)
    
    db.session.delete(data)
    db.session.commit()
    return jsonify(True)