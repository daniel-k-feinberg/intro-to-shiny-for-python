from shiny.express import ui, render, input, module
from shiny import reactive
import pandas as pd
from pathlib import Path
# from plots import temp_distribution, daily_error
import plots

infile = Path(__file__).parent / "weather.csv"
weather = pd.read_csv(infile)
weather["error"] = weather["observed_temp"] - weather["forecast_temp"]

## modules -------------

@module
def card_module(input, output, session, title, fn):
    with ui.card():
        ui.card_header(title)
        @render.plot
        def _plot_out():
            return fn()

## server ------------------

@reactive.calc
def filtered_data():
    df = weather.copy()
    df = df[df["city"].isin(input.cities())]
    df["date"] = pd.to_datetime(df["date"])
    dates = pd.to_datetime(input.dates())
    df = df[(df["date"] > dates[0]) & (df["date"] <= dates[1])]
    return df

## ui ------------------

ui.page_opts(title = "Weather error")
with ui.layout_sidebar():
    with ui.sidebar():
        ui.input_date_range("dates", "Date", start="2022-01-01", end="2022-01-30")
        ui.input_selectize(
            "cities",
            "Select Cities",
            weather["city"].unique().tolist(),
            selected="BUFFALO",
            multiple=True,
        )
    with ui.navset_tab():        
        with ui.nav_panel("Error"):
            card_module(
                "card_1", 
                "Distribution", 
                # use lambda to make an inline function
                # this will delay execution of the reactive code
                # until in the reactive context of the module, 
                # i.e rendering the plot
                lambda: plots.temp_distribution(filtered_data())
            )
            card_module(
                "card_2", 
                "Error by day", 
                lambda: plots.daily_error(filtered_data(), input.alpha())
            )
            ui.input_slider(
                "alpha", "Plot Alpha", value=0.5, min=0, max=1
            )


        with ui.nav_panel("Data"):
            @render.data_frame
            def data():
                return filtered_data()

