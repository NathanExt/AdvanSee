"""
Módulo para buscar assets no banco PMOC usando tag e patrimônio
"""

import re
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
from modulos.pmoc.pmoc_models.pmoc_database import Notebook, Desktop
from modulos.pmoc.pmoc_config import CONFIG_PMOC


def clean_string(value):
    """
    Limpa strings removendo espaços em branco desnecessários
    """
    if value is None:
        return None
    
    if isinstance(value, str):
        # Remove espaços no início e fim, e substitui múltiplos espaços por um único
        cleaned = re.sub(r'\s+', ' ', str(value).strip())
        return cleaned if cleaned else None
    
    return value


def clean_search_params(tag, patrimony):
    """
    Limpa parâmetros de busca
    """
    clean_tag = clean_string(tag)
    clean_patrimony = clean_string(patrimony)
    
    return clean_tag, clean_patrimony


class PMOCSearch:
    def __init__(self):
        """Inicializa conexão com banco PMOC"""
        try:
            self.engine = create_engine(CONFIG_PMOC.DATABASE_URL_PMOC)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
        except Exception as e:
            print(f"Erro ao conectar com banco PMOC: {e}")
            self.session = None
    
    def extract_patrimony_from_hostname(self, hostname):
        """
        Extrai o patrimônio do hostname
        Exemplo: NBKMT001069 -> 001069
        """
        if not hostname:
            return None
        
        # Padrão para extrair números do final do hostname
        # Busca por 6 dígitos consecutivos no final
        match = re.search(r'(\d{6})$', hostname)
        if match:
            return match.group(1)
        
        # Fallback: busca por qualquer sequência de dígitos no final
        match = re.search(r'(\d+)$', hostname)
        if match:
            return match.group(1).zfill(6)  # Preenche com zeros à esquerda
        
        return None
    
    def search_by_individual_fields(self, tag, patrimony):
        """
        Busca individual por cada campo (TAG, TAG_UISA, PATRIMÔNIO) e combina resultados
        """
        if not self.session:
            return {'error': 'Conexão com banco PMOC não disponível'}
        
        # Limpar parâmetros de entrada
        clean_tag, clean_patrimony = clean_search_params(tag, patrimony)
        
        try:
            # Usar sets para evitar duplicatas baseado no ID
            notebook_ids = set()
            desktop_ids = set()
            all_notebooks = []
            all_desktops = []
            
            # Lista de termos de busca para cada campo
            search_terms = []
            if clean_tag:
                search_terms.append(clean_tag)
            if clean_patrimony:
                search_terms.append(clean_patrimony)
            
            print(f"Termos de busca: {search_terms}")
            
            for term in search_terms:
                # Busca 1: Por campo TAG em notebooks
                notebooks_by_tag = self.session.query(Notebook).filter(Notebook.tag == term).all()
                print(f"Notebooks por TAG '{term}': {len(notebooks_by_tag)}")
                
                # Busca 2: Por campo TAG_UISA em notebooks
                notebooks_by_tag_uisa = self.session.query(Notebook).filter(Notebook.tag_uisa == term).all()
                print(f"Notebooks por TAG_UISA '{term}': {len(notebooks_by_tag_uisa)}")
                
                # Busca 3: Por campo PATRIMÔNIO em notebooks
                notebooks_by_patrimony = self.session.query(Notebook).filter(Notebook.patrimony == term).all()
                print(f"Notebooks por PATRIMÔNIO '{term}': {len(notebooks_by_patrimony)}")
                
                # Combinar resultados de notebooks evitando duplicatas
                for nb_list in [notebooks_by_tag, notebooks_by_tag_uisa, notebooks_by_patrimony]:
                    for nb in nb_list:
                        if nb.id not in notebook_ids:
                            notebook_ids.add(nb.id)
                            all_notebooks.append(nb)
                
                # Busca 1: Por campo TAG em desktops
                desktops_by_tag = self.session.query(Desktop).filter(Desktop.tag == term).all()
                print(f"Desktops por TAG '{term}': {len(desktops_by_tag)}")
                
                # Busca 2: Por campo TAG_UISA em desktops
                desktops_by_tag_uisa = self.session.query(Desktop).filter(Desktop.tag_uisa == term).all()
                print(f"Desktops por TAG_UISA '{term}': {len(desktops_by_tag_uisa)}")
                
                # Busca 3: Por campo PATRIMÔNIO em desktops
                desktops_by_patrimony = self.session.query(Desktop).filter(Desktop.patrimony == term).all()
                print(f"Desktops por PATRIMÔNIO '{term}': {len(desktops_by_patrimony)}")
                
                # Combinar resultados de desktops evitando duplicatas
                for dt_list in [desktops_by_tag, desktops_by_tag_uisa, desktops_by_patrimony]:
                    for dt in dt_list:
                        if dt.id not in desktop_ids:
                            desktop_ids.add(dt.id)
                            all_desktops.append(dt)
            
            print(f"Total únicos encontrados - Notebooks: {len(all_notebooks)}, Desktops: {len(all_desktops)}")
            
            results = {
                'notebooks': [],
                'desktops': [],
                'total_found': 0,
                'search_details': {
                    'searched_terms': search_terms,
                    'notebooks_found': len(all_notebooks),
                    'desktops_found': len(all_desktops)
                }
            }
            
            # Processar resultados dos notebooks encontrados
            for notebook in all_notebooks:
                results['notebooks'].append({
                    'id': clean_string(notebook.id),
                    'model': clean_string(notebook.model),
                    'patrimony': clean_string(notebook.patrimony),
                    'manufacturer': clean_string(notebook.manufacturer),
                    'tag': clean_string(notebook.tag),
                    'tag_uisa': clean_string(notebook.tag_uisa),
                    'status': clean_string(notebook.status),
                    'owner': clean_string(notebook.owner),
                    'type': 'notebook',
                    'processor': clean_string(notebook.processor),
                    'ram_memory': clean_string(notebook.ram_memory),
                    'os_version': clean_string(notebook.os_version),
                    'contract_type': clean_string(notebook.contract_type),
                    'created_at': notebook.created_at.isoformat() if notebook.created_at else None,
                    'updated_at': notebook.updated_at.isoformat() if notebook.updated_at else None
                })
            
            # Processar resultados dos desktops encontrados
            for desktop in all_desktops:
                results['desktops'].append({
                    'id': clean_string(desktop.id),
                    'model': clean_string(desktop.model),
                    'patrimony': clean_string(desktop.patrimony),
                    'manufacturer': clean_string(desktop.manufacturer),
                    'tag': clean_string(desktop.tag),
                    'tag_uisa': clean_string(desktop.tag_uisa),
                    'status': clean_string(desktop.status),
                    'owner': clean_string(desktop.owner),
                    'type': 'desktop',
                    'processor': clean_string(desktop.processor),
                    'ram_memory': clean_string(desktop.ram_memory),
                    'os_version': clean_string(desktop.os_version),
                    'contract_type': clean_string(desktop.contract_type),
                    'created_at': desktop.created_at.isoformat() if desktop.created_at else None,
                    'updated_at': desktop.updated_at.isoformat() if desktop.updated_at else None
                })
            
            results['total_found'] = len(all_notebooks) + len(all_desktops)
            
            return results
            
        except Exception as e:
            print(f"Erro ao buscar no banco PMOC: {e}")
            return {'error': f'Erro ao buscar no banco PMOC: {str(e)}'}
    
    def search_asset_by_hostname_and_tag(self, hostname, tag):
        """
        Busca asset no PMOC usando hostname (para extrair patrimônio) e tag
        """
        patrimony = self.extract_patrimony_from_hostname(hostname)
        
        print(f"Buscando no PMOC - Hostname: {hostname}, Tag: {tag}, Patrimônio extraído: {patrimony}")
        
        return self.search_by_individual_fields(tag, patrimony)
    
    def get_asset_details(self, asset_id, asset_type):
        """
        Busca detalhes completos de um asset específico
        """
        if not self.session:
            return {'error': 'Conexão com banco PMOC não disponível'}
        
        try:
            if asset_type.lower() == 'notebook':
                asset = self.session.query(Notebook).filter_by(id=asset_id).first()
            elif asset_type.lower() == 'desktop':
                asset = self.session.query(Desktop).filter_by(id=asset_id).first()
            else:
                return {'error': 'Tipo de asset inválido'}
            
            if not asset:
                return {'error': 'Asset não encontrado'}
            
            return {
                'id': clean_string(asset.id),
                'model': clean_string(asset.model),
                'patrimony': clean_string(asset.patrimony),
                'manufacturer': clean_string(asset.manufacturer),
                'equipment_value': float(asset.equipment_value) if asset.equipment_value else None,
                'tag': clean_string(asset.tag),
                'tag_uisa': clean_string(asset.tag_uisa),
                'status': clean_string(asset.status),
                'owner': clean_string(asset.owner),
                'type': asset_type,
                'processor': clean_string(asset.processor),
                'ram_memory': clean_string(asset.ram_memory),
                'os_version': clean_string(asset.os_version),
                'os_architecture': clean_string(asset.os_architecture),
                'contract_type': clean_string(asset.contract_type),
                'rc': clean_string(asset.rc),
                'entry_note': clean_string(asset.entry_note),
                'date_home': asset.date_home.isoformat() if asset.date_home else None,
                'date_end': asset.date_end.isoformat() if asset.date_end else None,
                'last_inventory_date': asset.last_inventory_date.isoformat() if asset.last_inventory_date else None,
                'created_at': asset.created_at.isoformat() if asset.created_at else None,
                'updated_at': asset.updated_at.isoformat() if asset.updated_at else None,
                'updated_by': clean_string(asset.updated_by)
            }
            
        except Exception as e:
            print(f"Erro ao buscar detalhes do asset: {e}")
            return {'error': f'Erro ao buscar detalhes: {str(e)}'}
    
    def close(self):
        """Fecha a conexão com o banco"""
        if self.session:
            self.session.close()


# Função de conveniência para busca rápida
def search_pmoc_asset(hostname, tag):
    """
    Função de conveniência para buscar asset no PMOC
    """
    searcher = PMOCSearch()
    try:
        results = searcher.search_asset_by_hostname_and_tag(hostname, tag)
        return results
    finally:
        searcher.close()


# Função para testar a extração de patrimônio
def test_patrimony_extraction():
    """
    Testa a extração de patrimônio de diferentes formatos de hostname
    """
    test_cases = [
        'NBKMT001069',
        'DESKTOP123456',
        'PC-001234',
        'WORKSTATION987654',
        'LAPTOP-456789',
        'INVALID-HOST',
        'NODIGITS'
    ]
    
    searcher = PMOCSearch()
    
    print("Teste de extração de patrimônio:")
    for hostname in test_cases:
        patrimony = searcher.extract_patrimony_from_hostname(hostname)
        print(f"Hostname: {hostname:20} -> Patrimônio: {patrimony}")
    
    searcher.close()


if __name__ == "__main__":
    # Teste da funcionalidade
    test_patrimony_extraction()
    
    # Exemplo de uso
    print("\nTeste de busca:")
    result = search_pmoc_asset('NBKMT001069', 'TEST_TAG')
    print(f"Resultados encontrados: {result}") 