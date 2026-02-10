import pandas as pd
from sqlalchemy import create_engine
import os
import unidecode
from datetime import datetime

def clean_column_name(col):
    """Padroniza os nomes das colunas para formato SQL válido"""
    col = unidecode.unidecode(str(col))  # Remove acentos
    col = col.replace(' ', '_').lower()  # Espaços para underscores e caixa baixa
    for char in ['(', ')', '%', '/', '-', '.', ',', ';', '°', 'º', 'ª']:
        col = col.replace(char, '')
    while '__' in col:
        col = col.replace('__', '_')  # Remove underscores duplicados
    return col.strip('_')

# --- CONFIGURAÇÕES DO BANCO DE DADOS ---
DB_CONFIG = {
    'user': "",
    'password': "",
    'host': "",
    'port': ,
    'db': ""
}

# --- CONEXÃO COM O BANCO ---
try:
    engine = create_engine(
        f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['db']}",
        pool_pre_ping=True,
        connect_args={'connect_timeout': 10}
    )
    print("✅ Conexão com o banco de dados estabelecida com sucesso!")
except Exception as e:
    print(f"❌ Erro ao conectar ao banco de dados: {e}")
    exit()

# --- CAMINHO DO ARQUIVO ---
caminho_csv = r'Seu arquivo'

if not os.path.exists(caminho_csv):
    print(f"❌ Arquivo não encontrado: {caminho_csv}")
    exit()

# --- LEITURA E LIMPEZA DO CSV ---
try:
    # Leitura parcial para capturar nomes originais das colunas
    df_temp = pd.read_csv(caminho_csv, encoding='utf-8', sep=';', header=0, nrows=1)
    original_columns = df_temp.columns.tolist()

    df = pd.read_csv(
        caminho_csv,
        encoding='utf-8',
        sep=';',
        header=0,
        on_bad_lines='warn',
        dtype={'CEP': str},
        parse_dates=['Data de Transação'],
        dayfirst=True,
        thousands='.',
        decimal=','
    )

    df.columns = [clean_column_name(col) for col in df.columns]

    # Verificação da coluna de identificação
    coluna_chave = 'ndeg_do_cadastro_sql'  # Corrigido aqui
    if coluna_chave not in df.columns:
        print(f"\n❌ Erro: Coluna '{coluna_chave}' não encontrada após renomeação.")
        print("Colunas disponíveis:", df.columns.tolist())
        print("Colunas originais:", original_columns)
        exit()

    # Remove duplicatas
    df = df.drop_duplicates(subset=[coluna_chave], keep='last')

    print("\n✅ Dados carregados com sucesso!")
    print("📌 Colunas:", df.columns.tolist())
    print("📊 Total de registros:", len(df))

except Exception as e:
    print(f"\n❌ Erro ao processar o arquivo CSV: {e}")
    if 'df' in locals():
        print("\nColunas lidas:", df.columns.tolist())
    exit()

# --- PRÓXIMO PASSO: Inserção no banco ---
# Exemplo (descomente e edite conforme necessário):
# df.to_sql('nome_da_tabela', con=engine, if_exists='replace', index=False)
