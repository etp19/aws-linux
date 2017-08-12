from flask import Flask

from FlaskApp.views.auth import mod_auth as auth_module
from FlaskApp.views.restaurant import restaurant_b
from FlaskApp.views.menu_items import menu_b
from FlaskApp.views.api import api_b
from FlaskApp.views.front_end import index_b

app = Flask(__name__)

app.register_blueprint(auth_module)
app.register_blueprint(restaurant_b, url_prefix='/restaurants')
app.register_blueprint(menu_b)
app.register_blueprint(api_b, url_prefix='/restaurants/developers')
app.register_blueprint(index_b)


# app.debug = True
if __name__ == "__main__":
    app.run()
