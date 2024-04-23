# Example of getting multiple inputs from slider bars

import plotly.express as px
import plotly.graph_objects as go

# Dash: The Dash app class
# dcc:  Dash Core Components (things like slider bars, buttons, etc.)
# html: Dash HTML components (things like you would see in HTML, e.g. <div>, <p>, <h1>)

from dash import Dash, dcc, html, Input, Output, State, callback

from datetime import datetime as dt
import numpy as np

TITLE = 'Hello World!'
FIG_ID = 'my-first-figure'

LABEL_SIZE = 18

FREQ = 'sine-frequency'
# Actually, time between samples
SAMPLE_RATE = 'sample-rate'

DISPLAY_SUFFIX = '-display'

FUNC_DISPLAY = 'sine-params'

# Settings for the user input (text box)
USER_INPUT = {'id'   : 'sine-frequency',
              'type' : 'text',
              'init' : 1
              }

USER_INPUT = {FREQ : {'id'   : FREQ,
                      'min'  : 1,
                      'max'  : 6,
                      'step' : 1,
                      'init' : 1  
                      },
              SAMPLE_RATE: {'id': SAMPLE_RATE,
                            'min': 0.001,
                            'max': 0.1,
                            'step': 0.001,
                            'init': 0.01
                            }
                }

TAU = 2*np.pi

def run_app() -> None:
    my_app = Dash(__name__)
    print(f'Started running at {str(dt.now())}')
    
    # The title will appear as the browser tab name
    my_app.title = TITLE

    # Apply the layout
    apply_main_layout(my_app)

    # Run the app in debug mode
    # Don't have debug mode turned on when you send someone (i.e. Ron) your code
    my_app.run(debug=True)

    return

@callback(
        Output(component_id = FIG_ID,
               component_property='figure'
               ),
        Output(component_id=FUNC_DISPLAY,
              component_property='children'
              ),
        Input(component_id=FREQ,
              component_property='value'
              ),
        Input(component_id=SAMPLE_RATE,
              component_property='value'
              )
)
def make_figure(freq: str = 1, 
                time_between_samples: str = 0.01
                ) -> go.Figure:
    if freq == '':
        freq = 0
    freq = float(freq)
    x = np.arange(0, 10, time_between_samples)
    y = np.sin(TAU*freq*x)

    fig = px.scatter(None,x,y)

    fig.update_layout(
        margin={'t': 0},
        xaxis={
        'title': '$x$',
        'title_font_size': LABEL_SIZE
        },
        yaxis={
            'title': None
        }
        )
    
    # Since we can't rotate the existing y-label, add it this way
    fig.add_annotation(
        xref='paper',
        yref='paper',
        x=-0.03,
        y=0.5,
        text='$y$',
        font_size=LABEL_SIZE,
        showarrow=False
    )

    equation = f'$y=\sin({TAU*freq:.3f}x)$'
    return fig, equation

@callback(
        Output(component_id=FREQ+DISPLAY_SUFFIX,
               component_property='children'),
        Input(component_id=FREQ,
              component_property='value')
)
def echo_freq(val):
    return f'Freq: ${val}\cdot(2\pi)$'

@callback(
        Output(component_id=SAMPLE_RATE+DISPLAY_SUFFIX,
               component_property='children'),
        Input(component_id=SAMPLE_RATE,
              component_property='value'
              )
)
def echo_sample_rate(val):
    return f'Time between samples: {val}'

def apply_main_layout(app: Dash) -> None:
    content = []

    greeting = html.H1('Welcome to my website!')
    figure_title = html.H2('Here is a figure!')
    freq_slider = dcc.Slider(id=FREQ,
                             min=USER_INPUT[FREQ]['min'],
                             max=USER_INPUT[FREQ]['max'],
                             step=USER_INPUT[FREQ]['step'],
                             value=USER_INPUT[FREQ]['init']
                             )
    freq_display = dcc.Markdown(id = FREQ + DISPLAY_SUFFIX,
                                mathjax=True
                                )
    sample_slider = dcc.Slider(id=SAMPLE_RATE,
                               min=USER_INPUT[SAMPLE_RATE]['min'],
                               max=USER_INPUT[SAMPLE_RATE]['max'],
                               step=USER_INPUT[SAMPLE_RATE]['step'],
                               value=USER_INPUT[SAMPLE_RATE]['init'],
                               marks=None,
                               tooltip={'template': '{value}'}
                               )
    sample_display = dcc.Markdown(id=SAMPLE_RATE + DISPLAY_SUFFIX,
                                  mathjax=True
                                  )
    func_display = dcc.Markdown(id=FUNC_DISPLAY,
                                mathjax=True,
                                style={'text-align': 'center'}
                                )
    
    my_figure = dcc.Graph(id=FIG_ID,
                          figure=make_figure()[0],
                          mathjax = True
                          )

    content.append(greeting)
    content.append(html.Hr())
    content.append(figure_title)
    content.append(freq_display)
    content.append(freq_slider)
    content.append(sample_display)
    content.append(sample_slider)
    content.append(func_display)
    content.append(my_figure)

    layout = html.Div(id='main-div',
                      children = content
                      )
    app.layout = layout
    return


if __name__ == '__main__':
    run_app()