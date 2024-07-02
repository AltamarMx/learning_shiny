from shiny import App, render, ui, reactive
import enerhabitat.funciones as eh
from iertools.read import read_epw
import matplotlib.pyplot as plt
import enerhabitat.definitions as ehd
import numpy as np
from shared import sidebar
from enerhabitat.diatipico import *
import plotly.express as px
from shinywidgets import output_widget, render_plotly
from enerhabitat.calculate import solve_1d_Tfree
import plotly.graph_objects as go

# timezone = pytz.timezone('America/Mexico_City')
# timezone = pytz.FixedOffset(-300)



app_ui = ui.page_sidebar(
    ui.sidebar(
        sidebar(eh.lugares,ehd.months),
        ui.input_switch("correr", "Ejecutar", False)  

    ),
    ui.navset_tab("",
                  ui.nav_panel(
                      "Temperaturas",
                      ui.card(output_widget("plot_temperatura"),
                              full_screen=True
                              ),
                    ),
                  ui.nav_panel(
                      "Radiación",
                      ui.card(output_widget("plot_radiacion"),
                              full_screen=True
                              ),
                    ),
                  ui.nav_panel(
                      "Datos",
                      ui.card(ui.output_data_frame("df_resultados"),
                              full_screen=True
                              ),
                    )
    )
)


def server(input, output, session):
    @reactive.Calc
    def load_day():
        caracteristicas = eh.cargar_caracteristicas(input.lugar())
        epw = read_epw(caracteristicas["epw"],alias=True,year=2024,warns=False)
        absortancia = input.absortancia() #0.3
        surface_tilt = float(input.inclinacion() ) # ubicacion
        surface_azimuth = float(input.orientacion()) #270
        mes = str(input.mes()).zfill(2)

        timezone = pytz.FixedOffset(caracteristicas['timezone'])
        dia = calculate_day(
            epw,
            caracteristicas['lat'],
            caracteristicas['lon'],
            caracteristicas['alt'],
            mes,
            absortancia,
            surface_tilt,
            surface_azimuth,
            timezone
        )
        return dia
    
    @reactive.Calc
    def solve_heat_transfer():
        # dia = load_day()
        dia['Ti'] = dia.Tsa + np.random.random()  # Placeholder para tu cálculo real
        dia['Tse'] = dia.Tsa + np.random.random() + 3.  # Placeholder para tu cálculo real
        dia['Tsi'] = dia.Tsa + np.random.random() - 3  # Placeholder para tu cálculo real
        # return dia

    @render_plotly
    def plot_temperatura():
        dia = load_day()
        # dia = solve_heat_transfer()
        df = dia.reset_index().iloc[::600]
        columnas =  ["Tsa",'Ta','Ti']
        # if input.ejecutar():
        #     columnas = ["Tsa",'Ta','Ti',"Tse","Tsi"]
        # else:
        #     columnas = ["Tsa",'Ta','Ti']
        fig = px.line(df,x="index",y=columnas)
        fig.add_trace(go.Scatter(
                                x=df["index"], 
                                y=df['Tn'] + df['DeltaTn'], 
                                mode='lines',
                                showlegend=False , 
                                line=dict(color='rgba(0,0,0,0)')
                                )
        )

        fig.add_trace(go.Scatter(
                                x=df["index"], 
                                y=df['Tn'] -df['DeltaTn'], 
                                mode='lines',
                                showlegend=False , 
                                fill='tonexty',
                                line=dict(color='rgba(0,0,0,0)'),
                                fillcolor='rgba(0,255,0,0.3)'
                                )
        )

    # Personalizar el layout

        fig.update_layout(
            yaxis_title='Temperatura (°C)',
            legend_title='', 
            xaxis_title=''
        )

        return fig
    @render_plotly
    def plot_radiacion():
        dia = load_day()
        df = dia.reset_index().iloc[::600]
        fig = px.line(df,x="index",y=["Ig","Ib","Id","Is"])
        fig.update_layout(
            yaxis_title='Radiación (W/m2)',
            legend_title='',  # Quitar el título de la leyenda
            xaxis_title=''
        )
        fig.update_yaxes(range=[0, 1200])  #
 
        return fig

    @render.data_frame
    def df_resultados():
        dia = load_day()
        mes = dia.reset_index()
        mes['index'] = mes['index'].dt.strftime('%Y-%m-%d %H:%M:%S')  # Convertir a string legible


        return render.DataGrid(mes[['index','Tsa','Ta','Ig','Is']].iloc[::600].round(1))
    
app = App(app_ui, server)
