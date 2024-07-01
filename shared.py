from pathlib import Path
from shiny import ui


app_dir = Path(__file__).parent

def sidebar(lugares,months):
    return ui.accordion(
        ui.accordion_panel(
            "Lugar, mes, tipo",
            ui.input_select("lugar", "Lugar", choices=lugares),
            ui.input_select("mes", "Mes", choices=months),
            ui.input_selectize("inclinacion", "Tipo", {'90':"Muro", '0':"Techo"}),
            # ui.input_numeric("absortancia", "Absortancia", 0.3, min=0, max=1, step=0.01),
        ),
        ui.accordion_panel(
            "Color, orientación",
            ui.input_numeric("absortancia", "Absortancia", 0.3, min=0.01, max=1, step=0.01),
            ui.input_selectize("orientacion", "Orientación", {90.0:"Este", 270.0:"Oeste" }),          
            ),
        open=True
    )