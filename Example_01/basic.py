import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, dcc, html

from datetime import datetime as dt
import numpy as np

TITLE = "TITLE"
TAU = 2*np.pi
FIG_ID = "figure-one"

def run_app() -> None:
    my_app = Dash(__name__)
    print(f"Started running at {str(dt.now())}")
    
    my_app.title = TITLE
    apply_main_layout(my_app)
    my_app.run(debug = True)

def make_figure() -> go.Figure:
    x = np.linspace(0, 10, 500)
    y = np.sin(TAU*x)

    fig = px.scatter(None, x, y)

    return fig

def apply_main_layout(app: Dash) -> None:
    layout = html.Div(id = "main-div",
                      children = [html.H1("Welcome to my website"),
                                  html.Hr(),
                                  html.H2("Here is a figure"),
                                  dcc.Graph(id = FIG_ID, figure = make_figure())
                                  ]
                       

    )
    app.layout = layout
    return

if __name__ == "__main__":
    run_app()