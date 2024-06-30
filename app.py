from shiny import App, render, ui, reactive
import enerhabitat.funciones as eh
from iertools.read import read_epw
import matplotlib.pyplot as plt
import enerhabitat.definitions as ehd
import numpy as np


app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.input_select(
            "lugar", "Lugar", choices=eh.lugares
        ),
        ui.input_select(
            "mes", "Mes", choices=ehd.months
        ),
        ui.input_numeric(
            "absortancia", "Absortancia",0.3, min=0,max=1,step=0.01
        ),
        ui.input_select(
            "tipo", "Tipo", choices=["Muro","Techo"]
        ),
    ),
    ui.navset_tab("",
                  ui.nav_panel(
                      "Temperaturas",
                      ui.card(ui.output_plot("plot_temperatura"),
                              full_screen=True
                              ),
                    ),
                  ui.nav_panel(
                      "Radiación",
                      ui.card(ui.output_plot("plot_radiacion"),
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
    def caracteristics():
        caracteristicas = eh.cargar_caracteristicas(input.lugar())
        epw = read_epw(caracteristicas["epw"],alias=True,year=2024,warns=False)
        return epw

    @render.plot
    def plot_temperatura():
        epw = caracteristics()
        fig, ax = plt.subplots() 
        
        ax.plot(epw.To.loc[f"2024-{input.mes().zfill(2)}"])
    @render.plot
    def plot_radiacion():
        epw = caracteristics()
        fig, ax = plt.subplots() 
        
        ax.plot(epw.Ig.loc[f"2024-{input.mes().zfill(2)}"])
        ax.plot(epw.Ib.loc[f"2024-{input.mes().zfill(2)}"])
        ax.plot(epw.Id.loc[f"2024-{input.mes().zfill(2)}"])
    @render.data_frame
    def df_resultados():
        epw = caracteristics()
        mes = epw[["To","Ig","Ib","Id"]].loc[f"2024-{input.mes().zfill(2)}"]
        mes = mes.reset_index()
        mes['tiempo'] = mes['tiempo'].dt.strftime('%Y-%m-%d %H:%M:%S')  # Convertir a string legible

        return render.DataGrid(mes)
    
app = App(app_ui, server)
