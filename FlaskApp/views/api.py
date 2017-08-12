from flask import Blueprint, render_template, jsonify
from FlaskApp.database import db_session, MenuItem, Restaurant, RestaurantAddress
api_b = Blueprint('api_b', __name__)

# this module is complete.

@api_b.route('/')
def developer_page():
    """Created route for the official developer page
    where I explain how to use the api"""
    return render_template("api/developers.html")


@api_b.route('/<int:restaurant_id>/JSON')
def restaurant_info(restaurant_id):
    """reated route and function for api endpoint,
        it will be use to display restaurants info"""
    try:
        restaurants = db_session.query(Restaurant).filter_by(id=restaurant_id).one()
        restaurants_info = jsonify(restaurant_info=restaurants.serialize)
        return restaurants_info
    except:
        return "Info not found"


@api_b.route('/location/<int:restaurant_id>/JSON')
def restaurant_location(restaurant_id):
    """reated route and function for api endpoint,
        it will be use to display restaurants info"""
    try:
        address = db_session.query(RestaurantAddress).filter_by(restaurant_id=restaurant_id).one()
        restaurant_address = jsonify(location=address.serialize)
        return restaurant_address

    except:
        return "Info not found"


@api_b.route('/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    """Created route and function for api endpoint,
        it will be use to display every menu for each restaurant"""
    try:
        items = db_session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
        return jsonify(menu_items=[i.serialize for i in items])
    except:
        return "Info not found"


@api_b.route('/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def each_menu_json(restaurant_id, menu_id):
    """Created route and function for api endpoint,
        it will be use to display each menu individually"""
    try:
        item = db_session.query(MenuItem).filter_by(id=menu_id, restaurant_id=restaurant_id).one()
        return jsonify(MenuItem=item.serialize)

    except:
        return "Info not found"
