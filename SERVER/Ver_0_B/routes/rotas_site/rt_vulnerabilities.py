from flask import Blueprint, render_template
from models.database import db, Vulnerability

bp_vulnerabilities = Blueprint('vulnerabilities', __name__)

@bp_vulnerabilities.route('/vulnerabilities')
def vulnerabilities():
    vulnerabilities_list = Vulnerability.query.all()
    return render_template('vulnerabilities.html', vulnerabilities_list=vulnerabilities_list)


