from flask_wtf import FlaskForm, RecaptchaField, Recaptcha
from wtforms import StringField, SubmitField, PasswordField, DecimalField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange
from validators import UniqueRequired, VaildUsername, ValidPassword, ValidASIN, ValidSavings

class LoginForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired(), VaildUsername], id="username")
    password = PasswordField("Password:", validators=[DataRequired(), ValidPassword], id="password")

class RegisterForm(FlaskForm):
    username = StringField("Username:", validators=[DataRequired(), UniqueRequired, Length(min=5, max=25)], id="username")
    password = PasswordField("Password:", validators=[DataRequired(), Length(min=8)], id="password")
    captcha = RecaptchaField(validators=[Recaptcha(message="Please use the Captcha before proceeding")])
    confirmpassword = PasswordField("Confirm Password:", validators=[DataRequired(), EqualTo('password', message="Passwords don't match")], id="conpassword")

class AddAmazonForm(FlaskForm):
    amazonlink = StringField("Add A Product:", validators=[DataRequired(), ValidASIN], id="amazonlink")

class AddBudgetForm(FlaskForm):
    monthlyincome = DecimalField("Monthly Income:", validators=[DataRequired()])
    fixedexpenses = DecimalField("Fixed Expenses:", validators=[DataRequired()], places=2)
    percentsavings = DecimalField(r"% of income to save:", validators=[DataRequired(), NumberRange(min=1, max=99), ValidSavings])