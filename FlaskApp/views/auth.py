#IMPORTS FOR THIS STEP
import json
import random
import string
from functools import wraps

import httplib2
from flask import make_response
from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask import session as login_session
from FlaskApp.userhelp import get_user_id, create_user

mod_auth = Blueprint('auth', __name__)

# This module is complete


def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user_id' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('restaurant_b.show_restaurants'))
    return wrap


# Create anti-forgery state token
@mod_auth.route('/login/', methods=['GET'])
def show_login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('auth/login.html', STATE=state)


# facebook login
@mod_auth.route('/fbconnect', methods=['GET', 'POST'])
def fbconnect():
    """Login via Facebook OAuth"""
    print "I am here"
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = request.data

    app_id = json.loads(
        open('/var/www/FlaskApp/fb_client_secret.json', 'r').read())['web']['app_id']
    app_secret = json.loads(
        open('/var/www/FlaskApp/fb_client_secret.json', 'r').read())['web']['app_secret']
    url = ('https://graph.facebook.com/v2.8/oauth/access_token?'
           'grant_type=fb_exchange_token&client_id=%s&client_secret=%s'
           '&fb_exchange_token=%s') % (app_id, app_secret, access_token)
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)

    # Extract the access token from response
    token = 'access_token=' + data['access_token']

    # Use token to get user info from API.
    url = 'https://graph.facebook.com/v2.8/me?%s&fields=name,id,email' % token
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly
    # logout, let's strip out the information before the equals sign in
    # our token.
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = ('https://graph.facebook.com/v2.8/me/picture?%s&redirect=0'
           '&height=200&width=200') % token
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # Check if the user exists in the database. If not create a new user.
    user_id = get_user_id(login_session['email'])
    if user_id is None:
        user_id = create_user(login_session)
        print "I am creating a new user"
    login_session['user_id'] = user_id
    print "from here it should print a welcome message"
    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style="width: 300px; height: 300px; border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@mod_auth.route('/fbdisconnect')
@login_required
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = ('https://graph.facebook.com/%s/permissions?'
           'access_token=%s') % (facebook_id, access_token)
    http = httplib2.Http()
    result = http.request(url, 'DELETE')[1]
    if result == '{"success":true}':
        response = make_response(json.dumps('You are successfully logout'), 200)
        response.headers['Content-Type'] = 'application/json'
        del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        return response
    else:
        # For whatever reason, the given token was invalid.
        response = make_response(
            json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response



