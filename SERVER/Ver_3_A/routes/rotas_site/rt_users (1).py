from flask import Blueprint, render_template
from models.database import User, db
from flask import jsonify

bp_users = Blueprint('users', __name__)




def dados():
    users = User.query.all()
    # Adicionar dados para o gráfico de usuários por função
    user_role_data = db.session.query(User.role, db.func.count(User.id)).group_by(User.role).all()
    user_role_labels = [data[0] for data in user_role_data]
    user_role_values = [data[1] for data in user_role_data]
    return users,user_role_labels,user_role_values


@bp_users.route('/users')
def users():
    users,_,_ = dados()
    return render_template('users.html',users=users,)


@bp_users.route('/api/grafico')
def grafico():
    _,user_role_labels,user_role_values= dados()
    return jsonify({"labels": user_role_labels,"values": user_role_values})
