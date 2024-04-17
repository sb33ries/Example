import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, dcc, html, Input, Output, state, callback

from datetime import datetime as dt
import numpy as np

TITLE = "TITLE"
TAU = 2*np.pi
FIG_ID = "figure-one"
FREQ = "sin_freq"
SAMPLE_RATE = "sample-rate"
USER_INPUT = {"id": "sin_freq",
              "type": "text",
              "init": 1}
USER_INPUT = {FREQ: {"id": FREQ,
                     "min": 1,
                     "max": 6,
                     "step": 1,
                     "init": 1},
              SAMPLE_RATE: {"id": SAMPLE_RATE,
                            "min": 0.001,
                            "max": 0.1,
                            "step": 0.01,
                            "init": 0.01}}

def run_app() -> None:
    my_app = Dash(__name__)
    print(f"Started running at {str(dt.now())}")
    
    my_app.title = TITLE
    apply_main_layout(my_app)
    my_app.run(debug = True)

@callback(
        Output(component_id = FIG_ID,
               component_property = "figure"),
        Input(component_id = FREQ,
               component_property = "value"),
        Input(component_id = SAMPLE_RATE,
               component_property = "value")
)
def make_figure(freq: str = 1, time_between_samples: str = 0.01) -> go.Figure:
    if freq == "":
        freq = 0
    freq = float(freq)

    x = np.arange(0, 10, time_between_samples)
    y = np.sin(TAU*x*freq)

    fig = px.scatter(None, x, y)

    return fig

def apply_main_layout(app: Dash) -> None:
    layout = html.Div(id = "main-div",
                      children = [html.H1("Welcome to my website"),
                                  html.Hr(),
                                  html.H2("Here is a figure"),
                                  dcc.Slider(id = FREQ,
                                             min = USER_INPUT[FREQ]["min"],
                                             max = USER_INPUT[FREQ]["max"],
                                             step = USER_INPUT[FREQ]["step"],
                                             value = USER_INPUT[FREQ]["init"]),
                                  dcc.Slider(id = SAMPLE_RATE,
                                             min = USER_INPUT[SAMPLE_RATE]["min"],
                                             max = USER_INPUT[SAMPLE_RATE]["max"],
                                             step = USER_INPUT[SAMPLE_RATE]["step"],
                                             value = USER_INPUT[SAMPLE_RATE]["init"]),
                                  dcc.Graph(id = FIG_ID, figure = make_figure())
                                  ]
                       

    )
    app.layout = layout
    return

if __name__ == "__main__":
    run_app()