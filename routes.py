from run import app, db
from flask import render_template, session, redirect, request
from forms import LoginForm, RegisterForm, AddAmazonForm
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from helpers import login_required, get_ASIN
import requests
from bs4 import BeautifulSoup
import decimal

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
    data = None
    if form.validate_on_submit():
        #get simplified amazon link
        link = "https://www.amazon.com/"
        extension = get_ASIN(form.amazonlink.data)
        extension = extension.group(0)
        link = link + extension

        #scrape price and product title from page
        #gets amazon page
        page = requests.get(link, headers=app.config["REQUEST_HEADERS"])
        #initializes scraper
        soup = BeautifulSoup(page.content, "html.parser")

        #gets title and page
        title = soup.find(id="productTitle").get_text().strip()
        amazon_price_ids = ["price_inside_buybox", "priceblock_ourprice", "priceblock_dealprice", "price", "newBuyBoxPrice"]
        for id in amazon_price_ids:
            regprice = soup.find(id=id)
            if regprice:
                regprice = regprice.get_text().strip()
                break
        
        #converts price into decimal
        #takes the first of any $xprice - $yprice listings
        #and gets rid of the $
        regprice = regprice.split('-')[0].strip("$")
        print(regprice)
    return render_template("amazon.html", form=form, data=data)
