# Importar bibliotecas -----
import pandas as pd
from sqlite3 import connect

# Conexão com banco de dados SQLite
conexao_sql = connect(database = "dados/dados.db")

# Coleta dados brutos
tbl_brutos = pd.read_sql_query("SELECT * FROM tbl_brutos", con = conexao_sql)

# Tratamento de dados -----

# Limpa tabela DBNOMICS
dados_tratados = (
 tbl_brutos
 .filter(items = ["period", "country (label)", "indicator (label)", "value"])
 .rename(
     columns = {
         "period": "data",
         "country (label)": "pais",
         "indicator (label)": "variavel",
         "value": "valor"
         }
     )
 .replace(
     to_replace = {
         "variavel": {
             "Inflation, consumer prices (annual %)": "Inflação (%, anual)",
             "Deposit interest rate (%)": "Juros (%, depósito)",
             "GDP growth (annual %)": "PIB (%, cresc. anual)",
             "Official exchange rate (LCU per US$, period average)": "Câmbio (UMC/US$, média)",
             "Unemployment, total (% of total labor force) (national estimate)": "Desemprego (%, total)"
             }
         }
     )
 .dropna()
 .assign(
     data = lambda x: pd.to_datetime(x.data),
     valor = lambda x: x.valor.astype(float),
     pais = lambda x: x.pais.astype(str)
     )
 )

# dados_tratados.info()

# Armazenamento de dados ----

# Criar/armazenar tabela de dados no banco SQLite
dados_tratados.to_sql(
    name = "tbl_tratados",
    con = conexao_sql,
    if_exists = "replace",
    index = False
    )

# Encerrar a conexão SQL
conexao_sql.close()
