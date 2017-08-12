from flask import render_template, Blueprint

index_b = Blueprint('index_b', __name__)

# this module is complete


@index_b.route('/')
def index():
    return render_template("front_end/index.html")
