from flask import Blueprint, render_template
from models.database import db, Asset

bp_assets = Blueprint('assets', __name__)

@bp_assets.route('/assets')
def assets():
    assets = Asset.query.options(
        db.joinedload(Asset.category),
        db.joinedload(Asset.vendor),
        db.joinedload(Asset.location),
        db.joinedload(Asset.assigned_user)
    ).all()
    return render_template('assets.html', assets=assets)


