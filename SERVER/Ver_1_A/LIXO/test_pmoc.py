#!/usr/bin/env python3
"""
Script de teste para o módulo PMOC
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from modulos.pmoc.pmoc_main import PMOC
from modulos.pmoc.pmoc_notebook import notebook

def test_connection():
    """Testa a conexão com o banco de dados"""
    print("🔍 Testando conexão com o banco de dados...")
    
    try:
        pmoc = PMOC()
        if pmoc.session:
            print("✅ Conexão estabelecida com sucesso!")
            return True
        else:
            print("❌ Falha na conexão")
            return False
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def test_data_fetch():
    """Testa a busca de dados da API"""
    print("\n🔍 Testando busca de dados da API...")
    
    try:
        dados = notebook()
        if dados and isinstance(dados, list):
            print(f"✅ Dados obtidos com sucesso! Total de registros: {len(dados)}")
            if len(dados) > 0:
                print(f"   Primeiro registro: {dados[0].get('id', 'N/A')}")
            return True
        else:
            print("❌ Nenhum dado obtido ou formato inválido")
            return False
    except Exception as e:
        print(f"❌ Erro ao buscar dados: {e}")
        return False

def test_table_exists():
    """Testa se a tabela notebook existe"""
    print("\n🔍 Verificando se a tabela notebook existe...")
    
    try:
        from sqlalchemy import text
        pmoc = PMOC()
        print(pmoc.session)
        result = pmoc.session.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'notebook'
            );
        """))
        print(result)
        table_exists = result.scalar()
        
        if table_exists:
            print("✅ Tabela 'notebook' existe no banco de dados")
            return True
        else:
            print("❌ Tabela 'notebook' não existe")
            print("   Execute o script create_pmoc_tables.py primeiro")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar tabela: {e}")
        return False

def test_single_insert():
    """Testa a inserção de um único registro"""
    print("\n🔍 Testando inserção de um registro...")
    
    try:
        pmoc = PMOC()
        dados = notebook()
        
        if dados and len(dados) > 0:
            # Testar com o primeiro registro
            equip = pmoc.criar_notebook(dados[0])
            print(equip)
            if equip:
                pmoc.session.add(equip)
                pmoc.session.commit()
                print("✅ Registro inserido com sucesso!")
                
                # Limpar o registro de teste
                pmoc.session.delete(equip)
                pmoc.session.commit()
                print("   Registro de teste removido")
                return True
            else:
                print("❌ Falha ao criar objeto notebook")
                return False
        else:
            print("❌ Nenhum dado disponível para teste")
            return False
            
    except Exception as e:
        print(f"❌ Erro na inserção: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("🧪 Teste do Módulo PMOC")
    print("=" * 50)
    
    tests = [
        ("Conexão com banco", test_connection),
        ("Busca de dados da API", test_data_fetch),
        ("Existência da tabela", test_table_exists),
        ("Inserção de registro", test_single_insert)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no teste '{test_name}': {e}")
            results.append((test_name, False))
    
    # Resumo dos resultados
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram! O módulo PMOC está funcionando corretamente.")
        print("   Você pode agora executar a gravação completa dos dados.")
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam.")
        print("   Verifique os problemas acima antes de prosseguir.")

if __name__ == "__main__":
    main() 