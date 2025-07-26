from flask import Blueprint, render_template
from models.database import db, Patch

bp_patches = Blueprint('patches', __name__)

@bp_patches.route('/patches')
def patches():
    patches_list = Patch.query.all()
    return render_template('patches.html', patches_list=patches_list)

