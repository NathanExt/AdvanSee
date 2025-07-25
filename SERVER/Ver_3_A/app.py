



import os, logging, sys
from flask import Flask, render_template
from models.database import db, Organization, User, Asset, Vulnerability
from config import CONFIG
from routes.rotas_site import rt_config, rt_assets, rt_asset_categories, rt_asset_detail, rt_organizations, rt_vulnerabilities, rt_patches, rt_software, rt_vendors, rt_locations, rt_users, rt_pmoc, rt_asset_vulnerabilidades, rt_pmoc_search
from routes.rotas_agente import rt_agente_checkin

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

CAMINHO_PASTA_RAIZ = CONFIG.CAMINHO_LOG


app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

app.secret_key = CONFIG.SECRET_KEY

# Configuração dos bancos de dados
app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.DATABASE_URL_DEFAULT
app.config['SQLALCHEMY_BINDS'] = CONFIG.SQLALCHEMY_BINDS
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CONFIG.SQLALCHEMY_TRACK_MODIFICATIONS

app.config['UPLOAD_FOLDER'] = CONFIG.CAMINHO_PASTA_UPLOADS
app.config['DOWNLOAD_FOLDER'] = CONFIG.CAMINHO_PASTA_DOWNLOADS

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

# Inicializar banco de dados (única instância)
db.init_app(app)

# Registrar blueprints
app.register_blueprint(rt_asset_categories.bp_asset_categories)
app.register_blueprint(rt_asset_detail.bp_asset_detail)
app.register_blueprint(rt_organizations.bp_organizations)
app.register_blueprint(rt_vulnerabilities.bp_vulnerabilities)
app.register_blueprint(rt_agente_checkin.bp_agente_checkin)
app.register_blueprint(rt_patches.bp_patches)
app.register_blueprint(rt_software.bp_software)
app.register_blueprint(rt_vendors.bp_vendors)
app.register_blueprint(rt_locations.bp_locations)
app.register_blueprint(rt_users.bp_users)
app.register_blueprint(rt_assets.bp_assets)
app.register_blueprint(rt_pmoc.bp_pmoc)
app.register_blueprint(rt_asset_vulnerabilidades.bp_asset_vulnerabilidades)
app.register_blueprint(rt_pmoc_search.bp_pmoc_search)
app.register_blueprint(rt_config.bp_config)

@app.route('/')
def index():
    organization_count = Organization.query.count()
    user_count = User.query.count()
    asset_count = Asset.query.count()
    vulnerability_count = Vulnerability.query.count()

    asset_status_data = db.session.query(Asset.status, db.func.count(Asset.id)).group_by(Asset.status).all()
    chart_labels = [data[0] for data in asset_status_data]
    chart_values = [data[1] for data in asset_status_data]

    return render_template('index.html',
                           organization_count=organization_count,
                           user_count=user_count,
                           asset_count=asset_count,
                           vulnerability_count=vulnerability_count,
                           chart_labels=chart_labels,
                           chart_values=chart_values)


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
    


#VER_0_B