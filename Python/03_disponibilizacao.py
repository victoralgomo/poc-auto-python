# Importar bibliotecas -----
import pandas as pd
from sqlite3 import connect

# Conexão com banco de dados SQLite
conexao_sql = connect(database = "dados/dados.db")

# Coleta dados tratados
tbl_tratados = pd.read_sql_query("SELECT * FROM tbl_tratados", con = conexao_sql)

# Salvar tabela como um arquivo CSV
tbl_tratados.to_csv(path_or_buf = "aplicacao/dashboard/dados_disponibilizados.csv", index = False)