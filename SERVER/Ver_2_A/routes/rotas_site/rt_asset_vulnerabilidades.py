from flask import Blueprint, render_template, flash, redirect

bp_asset_vulnerabilidades    = Blueprint('asset_vulnerabilidades', __name__)

@bp_asset_vulnerabilidades.route('/asset_vulnerabilidades')
def asset_vulnerabilidades():
    return render_template('asset_vulnerabilidades.html')

