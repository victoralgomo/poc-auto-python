# Importação de bibliotecas
from shiny import App, ui, render
import pandas as pd
import plotnine as p9


# Importação de dados
dados = (
    pd.read_csv("aplicacao/dashboard/dados_disponibilizados.csv")
    .assign(
        data = lambda x: pd.to_datetime(x.data),
        index = lambda x: x.data
        )
    .set_index("index")
    )


# Objetos úteis para Interface do Usuário/Servidor
nomes_variaveis = dados.variavel.unique().tolist()
nomes_paises = dados.pais.unique().tolist()
datas = dados.data.dt.date


# Parte 1: Interface do Usuário ----
app_ui = ui.page_fluid(
    ui.panel_title("⚽ Macro Copa"),
    ui.hr(),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.p("Entra em campo a seleção de dados macroeconômicos! ⚽"),
            ui.p("Defina os times de países e indicadores, explore o jogo de visualizações e marque gol na análise de dados!"),
            ui.input_select(
                id = "btn_variavel",
                label = "Selecione uma variável:",
                choices = nomes_variaveis,
                selected = "PIB (%, cresc. anual)",
                multiple = False
            ),
            ui.input_date_range(
                id = "btn_periodo",
                label = "Filtre os anos:",
                start = "2000-01-01",
                end = datas.max(),
                min = datas.min(),
                max = datas.max(),
                format = "yyyy",
                startview = "year",
                language = "pt-BR",
                separator = "-"
            ),
            ui.input_radio_buttons(
                id = "btn_tipo_grafico",
                label = "Selecione o tipo do gráfico:",
                choices = ["Área", "Coluna", "Linha"],
                selected = "Linha"
            )
        ),
        ui.panel_main(
            ui.row(
                ui.column(
                    6,
                    ui.input_select(
                        id = "btn_pais1",
                        label = "Selecione o 1º país:",
                        choices = nomes_paises,
                        selected = "Brazil",
                        multiple = False
                    )
                ),
                ui.column(
                    6,
                    ui.input_select(
                        id = "btn_pais2",
                        label = "Selecione o 2º país:",
                        choices = nomes_paises,
                        selected = "Argetina",
                        multiple = False
                    )
                )
            ),
            ui.row(
                ui.column(6, ui.output_plot("plt_pais1")),
                ui.column(6, ui.output_plot("plt_pais2")),
            )
        )
    )
)



# Parte 2: Lógica de Servidor ----
def server(input, output, session):
    @output
    @render.plot
    def plt_pais1():

        variavel_selecionada = input.btn_variavel()
        pais_selecionado = input.btn_pais1()
        tipo_plt = input.btn_tipo_grafico()
        data_inicial = input.btn_periodo()[0]
        data_final = input.btn_periodo()[1]

        df1 = dados.query(
            "variavel == @variavel_selecionada and data >= @data_inicial and data <= @data_final and pais == @pais_selecionado"
            )

        plt1 = (
            p9.ggplot(data = df1) +
            p9.aes(x = "data", y = "valor") +
            p9.scale_x_date(date_labels = "%Y") +
            p9.ggtitle(pais_selecionado + " - " + variavel_selecionada) +
            p9.ylab("") +
            p9.xlab("Ano") +
            p9.labs(caption = "Dados: Banco Mundial | Elaboração: Análise Macro")
        )
        if tipo_plt == "Área":
            plt1 = (plt1 + p9.geom_area())
        elif tipo_plt == "Coluna":
            plt1 = (plt1 + p9.geom_col())
        elif tipo_plt == "Linha":
            plt1 = (plt1 + p9.geom_line())

        return plt1
    
    @output
    @render.plot
    def plt_pais2():

        variavel_selecionada = input.btn_variavel()
        pais_selecionado = input.btn_pais2()
        tipo_plt = input.btn_tipo_grafico()
        data_inicial = input.btn_periodo()[0]
        data_final = input.btn_periodo()[1]

        df2 = dados.query(
            "variavel == @variavel_selecionada and data >= @data_inicial and data <= @data_final and pais == @pais_selecionado"
            )

        plt2 = (
            p9.ggplot(data = df2) +
            p9.aes(x = "data", y = "valor") +
            p9.scale_x_date(date_labels = "%Y") +
            p9.ggtitle(pais_selecionado + " - " + variavel_selecionada) +
            p9.ylab("") +
            p9.xlab("Ano") +
            p9.labs(caption = "Dados: Banco Mundial | Elaboração: Análise Macro")
        )
        if tipo_plt == "Área":
            plt2 = (plt2 + p9.geom_area())
        elif tipo_plt == "Coluna":
            plt2 = (plt2 + p9.geom_col())
        elif tipo_plt == "Linha":
            plt2 = (plt2 + p9.geom_line())

        return plt2



# Parte 3: shiny app/dashboard
app = App(app_ui, server)

# shiny run aplicacao/dashboard/app.py --reload
# rsconnect deploy shiny . --title poc-shiny-python