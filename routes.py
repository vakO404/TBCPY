from ext import app, db
from models import User, Product , Delivery, Rating
from flask import Flask, redirect, render_template, flash, url_for, session, request
from forms import DeliveryForm, LoginForm, RegisterForm, CartForm, RatingForm
from flask_login import login_user, login_required, current_user, logout_user

@app.route("/")
def index():
        new_products = Product.query.all()
        return render_template("index.html", new_products = new_products)

@app.route("/deliveryy")
def deliveryy():

        return render_template('deliveryy.html')

@app.route('/delivery_users')
def submit_users():

    delivery_users = Delivery.query.all()
    return render_template("delivery_users.html", delivery_users = delivery_users)


@app.route("/register_users")
@login_required
def register_users():
    if not current_user.is_admin:
        flash("access denied", 'danger')
        return redirect("/")
    register_users = User.query.all()
    return render_template("users.html", register_users = register_users)


@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
        user = User.query.get(user_id)

        if user:
            db.session.delete(user)
            db.session.commit()
        else:
            print(f'User with id {user_id} does not exist.')

        return redirect("/")



@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    if 'cart' in session:
        session['cart'].remove(product_id)
        print("product deleted")
        session.modified = True
    return redirect(url_for('cart_page'))




@app.route("/log_in", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username==form.username.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['cart'] = []
            login_user(user)
            if user.is_admin:
                print('343')
                return redirect("/")
            else:
                app.logger.info("User login successful")
                return redirect("/")
        else:
            flash("Invalid username or password", "danger")

    return render_template("log_in.html", form=form)




@app.route("/logout", methods = ["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect("/log_in")


@app.route('/delete_product/<int:new_product_id>', methods=['POST', 'GET'])
@login_required
def delete_product(new_product_id):
    if not current_user.is_admin:
        flash("access denied", 'danger')
        return redirect("/")
    product = Product.query.get(new_product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect("/")



@app.route("/register", methods = ["GET", "POST"])
def register():
        form = RegisterForm()
        if form.validate_on_submit():
                new_users = User(username=form.username.data, password=form.password.data, is_admin=False)
                existing_user = User.query.filter_by(username=form.username.data).first()
                if existing_user:
                        flash("Username already taken, Please choose another one", "danger")
                        return redirect("/register")

                db.session.add(new_users)
                db.session.commit()

                return redirect("/log_in")
        print(form.errors)
        return render_template("register.html", form= form)




@app.route("/delivery", methods=["GET", "POST"])
def delivery():
    form = DeliveryForm()
    if form.validate_on_submit():
        delivery_user = Delivery(
            email = form.email.data,
            name = form.name.data,
            lastname = form.lastname.data,
            phone_number=form.phone_number.data,
            country=form.country.data,
            city=form.city.data,
            address=form.address.data,
            post_code=form.post_code.data
        )
        db.session.add(delivery_user)
        db.session.commit()
        return redirect("/deliveryy")

    return render_template("delivery.html", form=form)


@app.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):
    currentuserid = session["user_id"]
    product = Product.query.get_or_404(product_id)
    myratingrecord = Rating.query.filter(Rating.user_id == int(currentuserid), Rating.product_id == product_id).first()
    myrating = 0
    if myratingrecord:
        myrating = myratingrecord.rating
    cart_form = CartForm()
    rt = request.form.get('rating')
    rating_form = RatingForm(product_id = product_id, rating = myrating)

    if rt:
        parsedrating = int(rt)
        rating_form = RatingForm(product_id = product_id, rating = parsedrating)

    if cart_form.validate_on_submit() and cart_form.add_to_cart.data:
        if "cart" not in session:
            session["cart"] = []
        session["cart"].append(product_id)
        session.modified = True
        return redirect(url_for("cart_page"))
    if rating_form.validate_on_submit() and rating_form.submit.data:
        print("Form validated and submit button clicked.")
        user_id = session.get('user_id')
        if user_id is None:
            flash('You must be logged in to rate products.', 'danger')
            return redirect(url_for('log_in'))

        rating_value = rating_form.rating.data

        existing_rating = Rating.query.filter_by(user_id=user_id, product_id=product_id).first()
        if existing_rating:
            existing_rating.rating = rating_value

        else:
            new_rating = Rating(user_id=user_id, product_id=product_id, rating=rating_value)
            db.session.add(new_rating)
            print("123")

        db.session.commit()

        ratings = Rating.query.filter_by(product_id=product_id).all()
        avg_rating = sum(r.rating for r in ratings) / len(ratings)

        product.rating = avg_rating
        product.rating_count = len(ratings)
        db.session.commit()

        return redirect(url_for("index"))

    return render_template('product.html', product=product, rating_form=rating_form, cart_form=cart_form)


@app.route('/cart', methods=['GET', 'POST'])
def cart_page():
    form = CartForm()
    cart = session.get('cart', [])
    products = Product.query.filter(Product.id.in_(cart)).all()
    total_price = sum(product.price for product in products)
    return render_template('cart.html', products=products, form = form, total_price=total_price)




