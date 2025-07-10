from flask import Blueprint, render_template
from models.database import db, Organization

bp_organizations = Blueprint('organizations', __name__) 

@bp_organizations.route('/organizations')
def organizations():
    organizations = Organization.query.all()
    return render_template('organizations.html', organizations=organizations)

