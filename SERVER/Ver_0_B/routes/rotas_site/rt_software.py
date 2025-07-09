from flask import Blueprint, render_template
from models.database import db, Software

bp_software = Blueprint('software', __name__)

@bp_software.route('/software')
def software():
    software_list = Software.query.all()
    return render_template('software.html', software_list=software_list)
