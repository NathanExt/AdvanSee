"""
Rota para testar a funcionalidade de busca no banco PMOC
"""

from flask import Blueprint, render_template, request, jsonify
from modulos.pmoc.pmoc_search import search_pmoc_asset, PMOCSearch

bp_pmoc_search = Blueprint('pmoc_search', __name__)

@bp_pmoc_search.route('/pmoc/search')
def pmoc_search_page():
    """Página para testar busca no PMOC"""
    return render_template('pmoc_search.html')

@bp_pmoc_search.route('/pmoc/search/api', methods=['GET', 'POST'])
def pmoc_search_api():
    """API para buscar assets no PMOC"""
    try:
        if request.method == 'POST':
            data = request.get_json()
            hostname = data.get('hostname', '')
            tag = data.get('tag', '')
        else:
            hostname = request.args.get('hostname', '')
            tag = request.args.get('tag', '')
        
        if not hostname and not tag:
            return jsonify({'error': 'Hostname ou tag devem ser fornecidos'}), 400
        
        # Buscar no PMOC
        results = search_pmoc_asset(hostname, tag)
        
        # Adicionar informações extras de patrimônio
        if results and 'error' not in results:
            searcher = PMOCSearch()
            try:
                extracted_patrimony = searcher.extract_patrimony_from_hostname(hostname)
                results['extracted_patrimony'] = extracted_patrimony
                results['search_params'] = {
                    'hostname': hostname,
                    'tag': tag,
                    'patrimony_extracted': extracted_patrimony
                }
            finally:
                searcher.close()
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': f'Erro na busca: {str(e)}'}), 500

@bp_pmoc_search.route('/pmoc/asset/<asset_type>/<asset_id>')
def pmoc_asset_details(asset_type, asset_id):
    """Detalhes de um asset específico do PMOC"""
    try:
        searcher = PMOCSearch()
        try:
            details = searcher.get_asset_details(asset_id, asset_type)
            return jsonify(details)
        finally:
            searcher.close()
            
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar detalhes: {str(e)}'}), 500

@bp_pmoc_search.route('/pmoc/test/patrimony')
def test_patrimony_extraction():
    """Testa extração de patrimônio de diferentes hostnames"""
    try:
        test_cases = [
            'NBKMT001069',
            'DESKTOP123456',
            'PC-001234',
            'WORKSTATION987654',
            'LAPTOP-456789',
            'SERVER-012345',
            'INVALID-HOST',
            'NODIGITS',
            'HOST123',
            'COMPUTER000001'
        ]
        
        searcher = PMOCSearch()
        results = []
        
        try:
            for hostname in test_cases:
                patrimony = searcher.extract_patrimony_from_hostname(hostname)
                results.append({
                    'hostname': hostname,
                    'patrimony': patrimony,
                    'extraction_success': patrimony is not None
                })
        finally:
            searcher.close()
        
        return jsonify({
            'test_results': results,
            'total_cases': len(test_cases),
            'successful_extractions': len([r for r in results if r['extraction_success']])
        })
        
    except Exception as e:
        return jsonify({'error': f'Erro no teste: {str(e)}'}), 500 