import plotly.express as px
import plotly.graph_objects as go

from dash import Dash, html, dcc, Input, Output, State, callback

from datetime import datetime as dt
import pandas as pd
import numpy as np

from plotly.data import gapminder
data = gapminder()
#-----------------------------------------------------------------------------

# ToDo:
#   - Slider bar labels are too small
#   - More customization in the tooltips
#   - Button for the log-x axis not yet implemented

TITLE           = 'Gapminder'

YEAR_SLIDER     = 'year-slider'
HIST_ID         = 'hist'
MAP_ID          = 'main-map'

VAL             = 'value'
FIG             = 'figure'

METRIC_DROPDOWN = 'metric-dropdown'
LOG_X           = 'logarithmic-x'

METRICS = {
    'lifeExp'   : 'Life Expectancy',
    'pop'       : 'Population',
    'gdpPercap' : 'GDP per capita'
    }

DEFAULTS = {
    'metric_id'   : 'lifeExp',
    'metric_name' : METRICS['lifeExp']
    }

def run_app():
    print(f'''I am located at {__file__} 
          and I started running at {str(dt.now())}''')
    app = Dash(__name__)
    app.title=TITLE
    apply_main_layout(app)
    app.run(debug=True)
    return

def get_default_df() -> pd.DataFrame:
    idx = data['year'] == data['year'].min()
    return data[idx]

def get_default_metric_id() -> str:
    return list(METRICS.keys())[0]

def get_metric_key(metric_name: str) -> str:
    for key, value in METRICS.items():
        if metric_name == value:
            return key
    raise ValueError(f'{metric_name} not in METRICS')

@callback(
        Output(component_id=MAP_ID,
               component_property=FIG,
               ),
        Output(component_id=HIST_ID,
               component_property=FIG
               ),
        Input(component_id=YEAR_SLIDER,
              component_property=VAL
              ),
        Input(component_id=METRIC_DROPDOWN,
              component_property='value'
              )
)
def get_current(year: int = None,
                metric_id: str = None
                ) -> pd.DataFrame:
    if year is None:
        data_year = get_default_df()
    else:
        data_year = data[data['year'] == year]
    
    if metric_id is None:
        metric_id = get_default_metric_id()

    map_year = world_map(metric_id, data_year)
    hist_year = world_distribution(metric_id, data_year)
    return map_year, hist_year

def world_map(metric_name: str,
              df_year: pd.DataFrame,
              ) -> go.Figure:

    metric_id = get_metric_key(metric_name)

    fig = px.choropleth(data_frame=df_year,
                        locations='iso_alpha',
                        color=metric_id,
                        hover_name='country',
                        hover_data={'iso_alpha': False},
                        #animation_frame='year',
                        range_color = [0, data[metric_id].max()],
                        labels={metric_id: metric_name, 'year': 'Year'}
                    )
    fig.update_layout(
        margin={
            't': 0, 'b': 0
            },
        coloraxis = {
            'colorbar': {
                'len': 0.7,
                'y': 0.15,
                'yanchor': 'bottom'
                }
            }
            )
    return fig

def world_distribution(metric_name: str = None,
                       df_year: pd.DataFrame = None
                       ) -> go.Figure:
    
    metric_id = get_metric_key(metric_name)

    fig = px.histogram(data_frame=df_year[metric_id],
                       range_x=[data[metric_id].min(), data[metric_id].max()]
                       )
    
    # https://community.plotly.com/t/histogram-bin-size-with-plotly-express/38927/4
    #fig.update_traces() <- good place to use get_clean_bins
    fig.update_layout(margin={'t': 0, 'b': 0},
                      bargap=0.1,
                      yaxis_title='# of countries',
                      xaxis_title=metric_name,
                      showlegend=False
                      )
    return fig

#=============================================================================
def apply_main_layout(app: Dash) -> None:
    content = []

    header = html.H1(id='header',
                     children='Gapminder Dashboard'
                     )

    year_slider = dcc.Slider(id=YEAR_SLIDER,
                     min=1952,
                     max=2007,
                     step=5,
                     value=1952,
                     updatemode='drag',
                     marks = {str(year): str(year) for year in data['year'].sort_values().unique()}
                     )
    
    metric_dropdown = dcc.Dropdown(id=METRIC_DROPDOWN,
                                   options=list(METRICS.values()),
                                   value=DEFAULTS['metric_name']
                                   )
    
    main_map = dcc.Graph(id=MAP_ID,
                         figure=world_map(metric_name=DEFAULTS['metric_name'],
                                          df_year=get_default_df()
                                          ),
                         #responsive=True,
                         style={
                             'width': '90%', 
                             'height': '70vh',
                             'margin-top': '0px',
                             'margin-bottom': '0px'
                             },
                         config={
                             'displayModeBar': False,
                             'scrollZoom': False,
                             #'autosizable': True
                             }
                         )
    world_dist = dcc.Graph(id=HIST_ID,
                           figure=world_distribution(metric_name=DEFAULTS['metric_name'],
                                                     df_year=get_default_df()
                                                     ),
                           style={
                               'width': '90%', 
                               'height': '30vh',
                               'margin-top': '0px',
                               'margin-bottom': '0px'
                               },
                          )
    
    logarithmic_x = dcc.Checklist(id='LOG_X',
                                  options=['Logarithmic x-axis']
                                  )
    
    content.append(header)
    content.append(html.Hr())
    content.append(metric_dropdown)
    content.append(year_slider)
    content.append(world_dist)
    content.append(logarithmic_x)
    content.append(main_map)
    content.append(html.Hr())

    layout = html.Div(id            = 'main-layout',
                      style         = {
                                        'margin' : 'auto',
                                        'width'  : '75%'
                                    },
                      children = content
                      )
    app.layout = layout
    return

if __name__ == '__main__':
    run_app()