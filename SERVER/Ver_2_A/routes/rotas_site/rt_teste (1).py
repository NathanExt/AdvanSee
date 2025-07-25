from flask import Blueprint, render_template, flash, redirect, request, url_for
from models.database import db, Asset, AssetSoftware, AssetVulnerability, AssetPatch, Agent, AssetHistory, InstalledSoftware, NetworkInterface, WindowsUpdate, PmocAsset # Importar novos modelos
from comand.comands import COMANDOS # Supondo que 'comand' é um módulo no seu projeto
from modulos.pmoc.pmoc_search import search_pmoc_asset
import os


bp_teste = Blueprint('teste', __name__)

@bp_teste.route('/teste')
def teste():
    return render_template('teste.html')



@bp_teste.route('/teste/info_asset', methods=['POST'])
def info_asset():

    assets_query = Asset.query
    return render_template('teste.html', assets=assets_query)
    