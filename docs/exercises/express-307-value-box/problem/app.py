from shiny.express import ui, render, input
from shiny import reactive
import pandas as pd
from pathlib import Path
import plots

infile = Path(__file__).parent / "weather.csv"
weather = pd.read_csv(infile)
weather["error"] = weather["observed_temp"] - weather["forecast_temp"]

            

ui.page_opts(title = "Weather error")

with ui.layout_sidebar():
    with ui.sidebar():
        ui.input_date_range("dates", "Date", start="2022-01-01", end="2022-01-30"),
        ui.input_selectize(
            "cities",
            "Select Cities",
            weather["city"].unique().tolist(),
            selected="BUFFALO",
            multiple=True,
        )
    with ui.navset_tab():
        with ui.nav_panel("Error"):    
            with ui.layout_columns():
                
                # insert a value box for hot days
                    @render.text
                    def hot_days():
                        hot_days = filtered_data()["error"] > 0
                        return sum(hot_days)
                        
                # insert a value box for cold days
                    @render.text
                    def cold_days():
                        hot_days = filtered_data()["error"] < 0
                        return sum(hot_days)

                # insert a value box for mean error
                    @render.text
                    def mean_error():
                        mean_error = filtered_data()["error"].mean()
                        return round(mean_error, 2)

            with ui.layout_columns():
                with ui.card():
                    ui.card_header("Distribution"),
                    @render.plot
                    def error_distribution():
                        return plots.temp_distribution(filtered_data())
                    
                with ui.card():
                    ui.card_header("Error by day")
                    @render.plot
                    def error_by_day():
                        return plots.daily_error(filtered_data(), input.alpha())
                    ui.input_slider("alpha", "Plot Alpha", value=0.5, min=0, max=1)
        
        with ui.nav_panel("Data"):
            @render.data_frame
            def data():
                return filtered_data()


@reactive.Calc
def filtered_data() -> pd.DataFrame:
    df = weather.copy()
    df = df[df["city"].isin(input.cities())]
    df["date"] = pd.to_datetime(df["date"])
    dates = pd.to_datetime(input.dates())
    df = df[(df["date"] > dates[0]) & (df["date"] <= dates[1])]
    return df



