from flask import session, redirect
from functools import wraps
import re
import requests
from bs4 import BeautifulSoup
from run import app
from decimal import Decimal
from matplotlib import pyplot as plt
from flask import session
from datetime import datetime
import os

#decorator for login validation
def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

#Gets shortened amazon link extension
#use ASIN.group(0) to get the full extension
def get_ASIN(url):
    ASIN = re.search('(?:dp|o|gp|-)\/(B[0-9]{2}[0-9A-Z]{7}|[0-9]{9}(?:X|[0-9]))', url)
    if ASIN: ASIN.group().split('/')[1]
    else: raise Exception("Not a valid link")
    return ASIN

#scrape price and product title from page
def get_amzn_data(link):
    #gets amazon page
    page = requests.get(link, headers=app.config["REQUEST_HEADERS"])
    #initializes scraper
    soup = BeautifulSoup(page.content, "lxml")

    #gets title and page
    try:
        title = soup.find(id="productTitle").get_text().strip()
    except:
        title = "Title Not Found"
    amazon_price_ids = ["price_inside_buybox", "priceblock_ourprice", "priceblock_dealprice", "price", "newBuyBoxPrice"]
    for id in amazon_price_ids:
        regprice = soup.find(id=id)
        print(regprice)
        if regprice:
            regprice = regprice.get_text().strip()
            break
    
    
    return {"title":title,"regprice":regprice}


#takes in an integer x and returns a Decimal object 0.0x
def percentify(x):
    if int(x) < 10:
        percent = f"0.0{x}"
    else:
        percent = f"0.{x}"
    return Decimal(percent)

#takes in a SQLALCHEMY Budget object, saves a pie chart in static/images/budget_charts
def make_budget_chart(budget):

    plt.style.use("fivethirtyeight")
    labels = ["Fixed expenses", "Saving Money", "Spending Money"]
    slices = [budget.fixed_expenses, budget.saving_money, budget.spending_money]
    
    plt.pie(slices, labels=labels, wedgeprops={"edgecolor": "black"}, autopct='%1.1f%%')

    plt.title("My Budget")
    plt.tight_layout()
    now = datetime.now()
    plt.savefig(f"static/images/budget_charts/{session['user_id']}{now.year}{now.month}{now.day}{now.hour}{now.minute}.png")

def is_negative(x):
    if x < 0:
        return True
    return False

def usd(x):
    return "${0:.2f}".format(x)