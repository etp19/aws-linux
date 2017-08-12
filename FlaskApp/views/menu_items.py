# flask imports
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask import session as login_session
from FlaskApp.views.auth import login_required
from FlaskApp.database import db_session, MenuItem, Restaurant

from FlaskApp.forms.menu_items import MenuItems

menu_b = Blueprint('menu_b', __name__)


@menu_b.route('/restaurants/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
@login_required
def create_menu_restaurant(restaurant_id):
    """Created route and function to create new menu items
        for each restaurant"""
    if Restaurant.user_creator(login_session['user_id'], restaurant_id):
        form = MenuItems()
        if form.validate_on_submit():
            new_item = MenuItem(name=form.name.data,
                                price=form.price.data,
                                course=form.course.data,
                                description=form.description.data,
                                restaurant_id=restaurant_id,
                                user_id=login_session['user_id'])
            db_session.add(new_item)
            db_session.commit()
            return redirect(url_for('restaurant_b.restaurant_detail', restaurant_id=restaurant_id))
        else:
            return render_template('menu_item/newMenuItem.html', form=form, restaurant_id=restaurant_id)
    else:
        flash("You cannot made any changes, make your own restaurant and try again")
        return redirect(url_for('restaurant_b.show_restaurants'))


@menu_b.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_menu_item(restaurant_id, menu_id):
    """Created route and function to edit each menu item in a restaurant"""
    if Restaurant.user_creator(login_session['user_id'], restaurant_id):
        menu = db_session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).first()
        form = MenuItems()
        if form.validate_on_submit():
            menu.name = form.name.data
            menu.price = form.price.data
            menu.course = form.course.data
            menu.description = form.description.data
            db_session.add(menu)
            db_session.commit()
            return redirect(url_for('restaurant_b.restaurant_detail', restaurant_id=restaurant_id))
        else:
            form.description.data = menu.description
            return render_template("menu_item/editMenuItem.html", form=form, menu=menu,
                                   restaurant_id=restaurant_id, menu_id=menu_id)
    else:
        flash("You cannot made any changes, make your own restaurant and try again")
        return redirect(url_for('restaurant_b.show_restaurants'))


@menu_b.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_menu_item(restaurant_id, menu_id):
    """Created route and function to delete a menu item"""
    if Restaurant.user_creator(login_session['user_id'], restaurant_id):
        menu = db_session.query(MenuItem).filter_by(restaurant_id=restaurant_id, id=menu_id).first()
        if request.method == 'POST':
            db_session.delete(menu)
            db_session.commit()
            return redirect(url_for('restaurant_b.show_restaurants'))

        return render_template("menu_item/deleteMenuItem.html", menu=menu, restaurant_id=restaurant_id)

    else:
        flash("You cannot made any changes, make your own restaurant and try again")
        return redirect(url_for('restaurant_b.show_restaurants'))
