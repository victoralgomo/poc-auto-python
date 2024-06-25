# Importar bibliotecas ----
import dbnomics
from sqlite3 import connect
import os

# Coleta de dados ----

# Importar os dados da DBNOMICS (fonte Banco Mundial - WDI)
dados_brutos = dbnomics.fetch_series_by_api_link(
    api_link = "https://api.db.nomics.world/v22/series/WB/WDI?dimensions=%7B" +
    "%22indicator%22%3A%5B%22NY.GDP.MKTP.KD.ZG%22%2C%22FP.CPI.TOTL.ZG%22%2C%" +
    "22SL.UEM.TOTL.NE.ZS%22%2C%22FR.INR.DPST%22%2C%22PA.NUS.FCRF%22%5D%2C%22" +
    "frequency%22%3A%5B%22A%22%5D%2C%22country%22%3A%5B%22ARG%22%2C%22AUS%22" +
    "%2C%22BEL%22%2C%22BRA%22%2C%22CMR%22%2C%22CAN%22%2C%22CRI%22%2C%22HRV%2" +
    "2%2C%22DNK%22%2C%22ECU%22%2C%22GBR%22%2C%22FRA%22%2C%22DEU%22%2C%22GHA%" +
    "22%2C%22IRN%22%2C%22JPN%22%2C%22KOR%22%2C%22MEX%22%2C%22MAR%22%2C%22NLD" +
    "%22%2C%22POL%22%2C%22PRT%22%2C%22QAT%22%2C%22SAU%22%2C%22SEN%22%2C%22SR" +
    "B%22%2C%22ESP%22%2C%22CHE%22%2C%22TUN%22%2C%22USA%22%2C%22URY%22%2C%22E" +
    "MU%22%5D%7D&observations=1",
    max_nb_series = 999
    )

# Armazenamento de dados ----

# Criar/conectar a um banco de dados SQLite
conexao_sql = connect(database = "dados/dados.db")

# Criar/armazenar tabela de dados no banco SQLite
dados_brutos.to_sql(
    name = "tbl_brutos",
    con = conexao_sql,
    if_exists = "replace",
    index = False
    )

'''
import pandas as pd
pd.read_sql_query(sql = "SELECT * FROM tbl_brutos", con = conexao_sql)
'''

# Encerrar a conexão SQL
conexao_sql.close()