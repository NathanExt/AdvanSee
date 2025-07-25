from flask import Blueprint, render_template
from models.database import db, Location

bp_locations = Blueprint('locations', __name__)

@bp_locations.route('/locations')
def locations():
    locations = Location.query.all()
    return render_template('locations.html', locations=locations)

