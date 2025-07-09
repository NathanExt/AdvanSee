from flask import Blueprint, render_template
from modulos.pmoc.pmoc_main import PMOC
bp_pmoc = Blueprint('pmoc', __name__)

@bp_pmoc.route('/pmoc')
def pmoc():
    return render_template('pmoc.html')


@bp_pmoc.route('/pmoc_atualiza', methods=['GET'])
def pmoc_atualiza():
    a = PMOC()
    a.grava_dados()
    print('ATUALIZAR')
    return render_template('pmoc.html')