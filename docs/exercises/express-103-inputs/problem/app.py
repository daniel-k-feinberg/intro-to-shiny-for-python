from shiny.express import ui

accounts=[
    "Berge & Berge",
    "Fritsch & Fritsch",
    "Hintz & Hintz",
    "Mosciski and Sons",
    "Wolff Ltd",
]

ui.input_select(
  id = "account",
  label = "Account",
  choices = accounts
)

ui.input_radio_buttons(
  id = "variable",
  label = "Select a variable to plot",
  choices = {
    "prod_score": "Product Score",
    "training_score": "Training Score"
  } 
)