from run import app, db
from flask import render_template, session, redirect, request, jsonify
from forms import LoginForm, RegisterForm, AddAmazonForm, AddBudgetForm
from models import User, Product
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required, get_ASIN, get_amzn_data
import requests
from bs4 import BeautifulSoup
from decimal import Decimal
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
        return redirect('/')
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
    linkprefix = "https://www.amazon.com/"
    if form.is_submitted():
        if form.validate_on_submit():
            #get simplified amazon link
            extension = get_ASIN(form.amazonlink.data)
            extension = extension.group(0)
            link = linkprefix + extension

            #reset form
            form.amazonlink.data = ''

            #scrape price and product title from page
            productdata = get_amzn_data(link)
            
            #converts price into decimal
            #takes the first of any $xprice - $yprice listings and gets rid of the $
            productdata["regprice"] = productdata["regprice"].split('-')[0].strip("$")
            print(productdata["regprice"])

            #add product to database
            product = Product(session["user_id"], productdata["title"], Decimal(productdata["regprice"]), link)
            db.session.add(product)
            db.session.commit()
    
    #get data to display in table
    data = Product.query.filter_by(user_id=session["user_id"]).order_by(Product.date_created.desc()).all()
    print(data)

    #get sale data
    sales = []
    for item in data:
        #gets scrape data for item
        scrapeextension = get_ASIN(item.amznlink)
        scrapelink = linkprefix + scrapeextension.group(0)
        scrapedata = get_amzn_data(scrapelink)
        scrapedata["regprice"] = scrapedata["regprice"].strip("$")

        #if price are the same, do nothing
        if Decimal(scrapedata["regprice"]) == Decimal(item.price):
            sales.append("No sale")
        #if prices are higher, update to that higher price
        if Decimal(scrapedata["regprice"]) > Decimal(item.price):
            item.price = Decimal(scrapedata["price"])
            db.commit()
            sales.append("No sale")
        #if prices are lower, show a sale
        if Decimal(scrapedata["regprice"]) < Decimal(item.price):
            salepercent = str(1 - (Decimal(scrapedata["regprice"]) / Decimal(item.price))).strip("-")
            salepercent = f"{salepercent[2:4]}%"
            salepercent = salepercent.lstrip("0")
            sales.append(salepercent)

    return render_template("amazon.html", form=form, data=data, sales=sales)


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

@app.route("/amznhelp")
@login_required
def amznhelp():
    return render_template("amznhelp.html")

@app.route("/makebudget", methods=["GET", "POST"])
@login_required
def makebudget():
    form = AddBudgetForm()
    return render_template("makebudget.html", form=form)