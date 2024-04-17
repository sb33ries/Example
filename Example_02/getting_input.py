import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, dcc, html, Input, Output, callback

from datetime import datetime as dt
import numpy as np

TITLE = "TITLE"
TAU = 2*np.pi
FIG_ID = "figure-one"
USER_INPUT = {"id": "sin_freq",
              "type": "text",
              "init": 1

}

def run_app() -> None:
    my_app = Dash(__name__)
    print(f"Started running at {str(dt.now())}")
    
    my_app.title = TITLE
    apply_main_layout(my_app)
    my_app.run(debug = True)

@callback(
        Output(component_id = FIG_ID,
               component_property = "figure"),
        Input(component_id = USER_INPUT["id"],
               component_property = "value")
)
def make_figure(freq: str = 1) -> go.Figure:
    if freq == "":
        freq = 0
    freq = float(freq)
    
    x = np.linspace(0, 10, 500)
    y = np.sin(TAU*x*freq)

    fig = px.scatter(None, x, y)

    return fig

def apply_main_layout(app: Dash) -> None:
    layout = html.Div(id = "main-div",
                      children = [html.H1("Welcome to my website"),
                                  html.Hr(),
                                  html.H2("Here is a figure"),
                                  dcc.Input(id = USER_INPUT["id"],
                                            type = USER_INPUT["type"],
                                            value = USER_INPUT["init"]),
                                  dcc.Graph(id = FIG_ID, figure = make_figure())
                                  ]
                       

    )
    app.layout = layout
    return

if __name__ == "__main__":
    run_app()