from flask import Blueprint, render_template
from models.database import db, AssetCategory

bp_asset_categories = Blueprint('asset_categories', __name__)

@bp_asset_categories.route('/asset_categories')
def asset_categories():
    categories = AssetCategory.query.all()
    return render_template('asset_categories.html', categories=categories)
