from flask import session, redirect
from functools import wraps
import re
import requests
from bs4 import BeautifulSoup
from run import app
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

#use ASIN.group(0) to get the full extension
def get_ASIN(url):
    ASIN = re.search('(?:dp|o|gp|-)\/(B[0-9]{2}[0-9A-Z]{7}|[0-9]{9}(?:X|[0-9]))', url)
    if ASIN: ASIN.group().split('/')[1]
    else: raise Exception("Not a valid link")
    return ASIN

def get_amzn_data(link):
    #scrape price and product title from page
    #gets amazon page
    page = requests.get(link, headers=app.config["REQUEST_HEADERS"])
    #initializes scraper
    soup = BeautifulSoup(page.content, "lxml")

    #gets title and page
    title = soup.find(id="productTitle").get_text().strip()
    amazon_price_ids = ["price_inside_buybox", "priceblock_ourprice", "priceblock_dealprice", "price", "newBuyBoxPrice"]
    for id in amazon_price_ids:
        regprice = soup.find(id=id)
        if regprice:
            regprice = regprice.get_text().strip()
            break
    return {"title":title,"regprice":regprice}


