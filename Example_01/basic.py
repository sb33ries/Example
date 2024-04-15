import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, dcc, html

from datetime import datetime as dt
import numpy as np

TITLE = "TITLE"

def apply_main_layout(app: Dash) -> None:
    layout = html.Div(id = "main-div",
                      children = [html.H1("Welcome to my website"),
                                  html.Hr()
                                  ]
                       

    )
    app.layout = layout
    return

if __name__ == "__main__":
    my_app = Dash(__name__)
    print(f"Started running at {str(dt.now())}")
    
    my_app.title = TITLE
    apply_main_layout(my_app)
    my_app.run(debug = True)