# Wiseance

A riff on Wise + Finance, this small web app is all about saving and managing money. It's a combination of
a budgeting tool to keep track of spending money, and an amazon wishlist that gets the price of items, and
alerts you if there is a sale or price drop.

## Getting Started

Install python, preferably 3.7.4 from https://www.python.org/downloads/release/python-374/

clone the repository to your local machine

```
git clone https://github.com/anthonypapetti/Wiseance.git
```

Install the required packages from requirements.txt

```
pip install -r requirements.txt
```

Set a config.json file with a RECAPTCHA_PUBLIC_KEY and RECAPTCHA_PRIVATE_KEY

```
{
    "RECAPTCHA_PUBLIC_KEY":"#########################################",
    "RECAPTCHA_PRIVATE_KEY":"#########################################"
}
```

To create your database:
```
>>> from run import db
>>> db.create_all()
```

You're all set to run this project. Just run run.py and you're good to go!

## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Web Framework
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - Object-oriented SQL Framework
* [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) - Form validation
* [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - Web scraper
* [lxml](https://lxml.de/) - Alternative web scraper
* [matplotlib](https://matplotlib.org/) - Data visualisation


## Authors

* [**Anthony Papetti**](https://github.com/anthonypapetti)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/anthonypapetti/Wiseance/blob/master/LICENSE) file for details
