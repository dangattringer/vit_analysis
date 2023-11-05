import os.path as osp
import plotly.io as pio
import io
import dash
import dash_bootstrap_components as dbc

from dash import callback, dcc, html, register_page
from dash.dependencies import Input, Output
from lib.params import MODELS_DICT, MODELS, ARCHS

from .utils import gen_plots
from .summary_tabs import tab_1, tab_2

register_page(
    __name__,
    name='Summary',
    top_nav=True,
    path='/summary'
)


def layout():
    layout = dbc.Container([
        html.Div([
            html.H5("Attention Analysis",
                    className='mt-2 text-center'),
        ]),
        dbc.Tabs([
            dbc.Tab(label='distance', tab_id='distance-sum', children=tab_1),
            dbc.Tab(label='maps', tab_id='maps-sum', children=tab_2),
        ],
            active_tab="distance-sum",
        ),
    ], fluid=True)
    return layout


