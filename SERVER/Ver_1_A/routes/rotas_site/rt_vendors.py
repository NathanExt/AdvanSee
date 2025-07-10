from flask import Blueprint, render_template
from models.database import Vendor

bp_vendors = Blueprint('vendors', __name__)

@bp_vendors.route('/vendors')
def vendors():
    vendors = Vendor.query.all()
    return render_template('vendors.html', vendors=vendors)
