import json

with open("config.json") as f:
    keys = json.load(f)

DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "\x07\xaa\x82\x1a\x16\xaa\xfe\x80\xaa\xd6"
TEMPLATES_AUTO_RELOAD = True
WTF_CSRF_SECRET_KEY = 'rdyctfvgyhjkhnbgiudyrtuycivuobnhytuy2345678976543./'
REQUEST_HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"}
RECAPTCHA_PUBLIC_KEY = keys["RECAPTCHA_PUBLIC_KEY"]
RECAPTCHA_PRIVATE_KEY = keys["RECAPTCHA_PRIVATE_KEY"]