from shiny.express import ui

ui.input_select(
    id="account",
    label="Account",
    choices=[
    "Berge & Berge",
    "Fritsch & Fritsch",
    "Hintz & Hintz",
    "Mosciski and Sons",
    "Wolff Ltd",
]
)

ui.input_radio_buttons(
    "variable",
    "Select a variable to plot",
    choices={
        "prod_score": "Product Score", 
        "training_score": "Training Score"
    }
)