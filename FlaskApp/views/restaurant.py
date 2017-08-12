from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask import session as login_session
from FlaskApp.views.auth import login_required
from FlaskApp.database import db_session, MenuItem, Restaurant, RestaurantAddress

from sqlalchemy import desc

from FlaskApp.forms.restaurants import RestaurantForm

restaurant_b = Blueprint('restaurant_b', __name__)


@restaurant_b.route('/')
def show_restaurants():
    """Created route and function to display the
       restaurant list """
    restaurants = db_session.query(Restaurant).order_by(desc(Restaurant.name))
    if restaurants:
        if 'user_id' in login_session:
            print ('user_id in login_session')
            return render_template('restaurant/restaurants.html', restaurants=restaurants, hello="database found")
        else:
            print ('user_id not in login_session')
            return render_template('restaurant/restaurants.html', restaurants=restaurants)
    else:
        return render_template('restaurant/restaurants.html', restaurants=restaurants, hello="no database")


@restaurant_b.route('/<int:restaurant_id>/menu/')
@restaurant_b.route('/<int:restaurant_id>/')
def restaurant_detail(restaurant_id):
    """Created route and function to display the
        restaurant main page and menu individually"""
    try:
        restaurant = db_session.query(Restaurant).filter_by(id=restaurant_id).one()
        address = db_session.query(RestaurantAddress).filter_by(id=restaurant_id).one()
        items = db_session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
        return render_template("restaurant/restaurantownpage.html", restaurant=restaurant, items=items, address=address)

    except:
        return render_template("restaurant/restaurants.html", error="Restaurant Not Found")


@restaurant_b.route('/new', methods=['GET', 'POST'])
@login_required
def create_restaurant():
    form = RestaurantForm()

    if form.validate_on_submit():
        add_values = Restaurant(name=form.name.data,
                                phone=form.phone.data,
                                food_type=form.course.data,
                                email=form.email.data,
                                website=form.website.data,
                                description=form.description.data,
                                user_id=login_session['user_id'])
        db_session.add(add_values)
        db_session.commit()
        db_session.refresh(add_values)
        add_address = RestaurantAddress(street=form.street.data,
                                        city=form.city.data,
                                        state=form.state.data,
                                        zip_code=form.zip_code.data,
                                        restaurant_id=add_values.id)
        db_session.add(add_address)
        db_session.commit()
        flash("New restaurant Created")
        return redirect(url_for('.show_restaurants'))

    else:
        return render_template("restaurant/newRestaurant.html", form=form)


@restaurant_b.route('/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
@login_required
def delete_restaurant(restaurant_id):
    """Created route and function to delete restaurants individually"""
    if Restaurant.user_creator(login_session['user_id'], restaurant_id):
        restaurant = db_session.query(Restaurant).filter_by(id=restaurant_id).one()
        address = db_session.query(RestaurantAddress).filter_by(restaurant_id=restaurant.id).one()
        if request.method == 'POST':
            db_session.delete(address)
            db_session.delete(restaurant)
            db_session.commit()
            flash("Your Restaurant have been deleted")
            return redirect(url_for('.show_restaurants'))

        return render_template("restaurant/deleteRestaurant.html", restaurant=restaurant)
    else:
        flash("You cannot made any changes, make your own restaurant and try again")
        return redirect(url_for('.show_restaurants'))


@restaurant_b.route('/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
@login_required
def edit_restaurant(restaurant_id):
    """Created route and function to edit restaurants"""
    if Restaurant.user_creator(login_session['user_id'], restaurant_id):
        restaurant = db_session.query(Restaurant).filter_by(id=restaurant_id).one()
        address = db_session.query(RestaurantAddress).filter_by(restaurant_id=restaurant.id).one()
        form = RestaurantForm()
        if form.validate_on_submit():
            restaurant.name = form.name.data
            restaurant.phone = form.phone.data
            restaurant.email = form.email.data
            restaurant.course = form.course.data
            restaurant.description = form.description.data
            restaurant.website = form.website.data
            db_session.add(restaurant)

            db_session.commit()
            db_session.refresh(restaurant)
            address.street = form.street.data
            address.city = form.city.data
            address.state = form.state.data
            address.zip_code = form.zip_code.data
            db_session.add(address)
            db_session.commit()
            flash("Your restaurant have been edited successfully")
            return redirect(url_for('.show_restaurants'))
        else:
            form.description.data = restaurant.description
            return render_template("restaurant/editrestaurant.html", form=form, restaurant=restaurant, address=address)
    else:
        flash("You cannot made any changes, make your own restaurant and try again")
        return redirect(url_for('.show_restaurants'))
