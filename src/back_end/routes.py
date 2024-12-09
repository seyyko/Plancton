from flask import Blueprint, render_template
import scraping

# create a Blueprint
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

# add more routes for homework, test, note, ....
