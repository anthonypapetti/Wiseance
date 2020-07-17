from models import User
from wtforms.validators import ValidationError
from werkzeug.security import check_password_hash
import requests
import re

def UniqueRequired(form, field):
    otheruser = User.query.filter_by(username=field.data).first()
    if otheruser:
        raise ValidationError("Username Taken")

def VaildUsername(form, field):
    user = User.query.filter_by(username=field.data).first()
    print(user)
    if not user:
        raise ValidationError("Invalid Username")

def ValidPassword(form, field):
    user = User.query.filter_by(username=form.username.data).first()
    if user == None:
        return
    if not check_password_hash(user.password, field.data):
        raise ValidationError("Incorrect Password")

def ValidASIN(form, field):
    ASIN = re.search('(?:dp|o|gp|-)\/(B[0-9]{2}[0-9A-Z]{7}|[0-9]{9}(?:X|[0-9]))', field.data)
    if not ASIN: raise ValidationError("Not A Valid Amazon Link")

def ValidSavings(form, field):
    expense_percent = int(form.fixedexpenses.data) / int(form.monthlyincome.data)
    if int(field.data) < 10:
        savings_percent = '0' + field.data
    else:
        savings_percent = field.data

    if expense_percent + float('0.' + str(savings_percent)) > 1:
        raise ValidationError("Not enough money")
