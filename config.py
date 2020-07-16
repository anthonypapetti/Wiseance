import os

DEBUG = True
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = "\x07\xaa\x82\x1a\x16\xaa\xfe\x80\xaa\xd6"
TEMPLATES_AUTO_RELOAD = True
WTF_CSRF_SECRET_KEY = 'rdyctfvgyhjkhnbgiudyrtuycivuobnhytuy2345678976543./'
REQUEST_HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0"}
RECAPTCHA_PUBLIC_KEY = '6LezQa8ZAAAAAJuOt6g4SRSNNCuCNvg_UwPAHFM6'
RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY")