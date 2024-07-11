from flask_wtf import FlaskForm
from wtforms.fields import StringField,PasswordField, SelectField,SubmitField, IntegerField, HiddenField
from wtforms.validators import DataRequired,Length, Email,equal_to, NumberRange

class DeliveryForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    name = StringField("Name", validators=[DataRequired()])
    lastname = StringField("Lastname", validators=[DataRequired()])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=1, max=15)])
    country = SelectField('Country', choices=["choose country", "Georgia", "England", "USA", "Japan", "Italy"], validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired(), Length(min=1, max=50)])
    address = StringField('Address', validators=[DataRequired(), Length(min=1, max=100)])
    post_code = StringField('Post Code', validators=[DataRequired(), Length(min=3, max=10)])
    delivery = SubmitField('Delivery')


class RatingForm(FlaskForm):
    product_id = HiddenField('Product ID', validators=[DataRequired()])
    rating = IntegerField('Rating (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit Rating')

class CartForm(FlaskForm):
    add_to_cart = SubmitField('Add to Cart')
    remove_from_cart = SubmitField('Remove')
class RegisterForm(FlaskForm):
    email = StringField("email", validators=[DataRequired()])
    username = StringField("username", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired(), Length(min=7, max=20)])
    repeat_password = PasswordField("confirm password",validators=[DataRequired(), equal_to("password")])

    register = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("username",validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])

    login = SubmitField("Login")



