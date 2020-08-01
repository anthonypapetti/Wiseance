from run import app, db
from flask import render_template, session, redirect, request, jsonify
from forms import LoginForm, RegisterForm, AddAmazonForm, AddBudgetForm, BuyForm
from models import User, Product, Budget
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required, get_ASIN, get_amzn_data, percentify, make_budget_chart, is_negative, usd
import requests
from bs4 import BeautifulSoup
from decimal import Decimal
import decimal
from datetime import datetime

decimal.getcontext().prec = 2
app.jinja_env.filters["is_negative"] = is_negative
app.jinja_env.filters["usd"] = usd

@app.route("/")
def index():
    return render_template("landing.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        session["user_id"] = user.id
        session["username"] = user.username
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
        session["username"] = user.username
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
    if form.validate_on_submit():
        #Get data
        #amount of money to save
        saving_money = Decimal(form.monthlyincome.data) * percentify(form.percentsavings.data)
        #amount of money to spend
        spending_money = Decimal(form.monthlyincome.data) - Decimal(form.fixedexpenses.data) - saving_money

        #Save data to budget
        #check if data already exists
        otherbudget = Budget.query.filter_by(user_id=session["user_id"]).first()
        now = datetime.now()
        img_name =f"{session['user_id']}{now.year}{now.month}{now.day}{now.hour}{now.minute}.png"
        if otherbudget:
            #change data
            otherbudget.income = form.monthlyincome.data
            otherbudget.fixed_expenses = form.fixedexpenses.data
            otherbudget.saving_money = saving_money
            otherbudget.spending_money = spending_money
            otherbudget.spending_left = spending_money
            otherbudget.graph_link = img_name
            #commit changes
            db.session.commit()
            make_budget_chart(otherbudget)
        #if budget does not exist
        else:
            #create new budget
            mybudget = Budget(user_id=session["user_id"], income=form.monthlyincome.data, fixed_expenses=form.fixedexpenses.data, saving_money=saving_money,
            spending_money=spending_money, spending_left=spending_money, graph_link=img_name)

            db.session.add(mybudget)
            db.session.commit()
            make_budget_chart(mybudget)
        
        return redirect("/viewbudget")
    return render_template("makebudget.html", form=form)

@app.route("/viewbudget", methods=["GET", "POST"])
@login_required
def viewbudget():
    form = BuyForm()
    #get budget data
    mybudget = Budget.query.filter_by(user_id=session["user_id"]).first()
    if mybudget:
        img_path = f"images/budget_charts/{mybudget.graph_link}"
    else:
        img_path = None
    if form.validate_on_submit():
        mybudget.spending_left -= form.money.data
        db.session.commit()
    return render_template("viewbudget.html", form=form, img_path=img_path, data = mybudget)

@app.route("/resetbudget", methods=["GET", "POST"])
@login_required
def resetbudget():
    mybudget = Budget.query.filter_by(user_id=session["user_id"]).first()
    if mybudget:
        mybudget.spending_left = mybudget.spending_money
        db.session.commit()
        return jsonify("${0:.2f}".format(mybudget.spending_money))
    else:
        return jsonify(False)
