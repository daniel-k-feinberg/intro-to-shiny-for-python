from shiny.express import render, ui, input
import pandas as pd
from pathlib import Path
from data_import import df

ui.input_select(
    "account",
    "Account",
    choices=[
        "Berge & Berge",
        "Fritsch & Fritsch",
        "Hintz & Hintz",
        "Mosciski and Sons",
        "Wolff Ltd",
    ],
)


@render.data_frame
def table():
    # Remember that inputs are callable values, so whenever you refer to them
    # in rendering functions you need to call them (`input.account()` not `input.account`)
    account_subset = df[df["account"] == input.account()]
    account_counts = (
        account_subset.groupby("sub_account").size().reset_index(name="counts")
    )
    return account_counts
