import dash_bootstrap_components as dbc
from dash import html, register_page
from .analysis_tabs import tab_1, tab_2


register_page(
    __name__,
    name='Analysis',
    top_nav=True,
    path='/analysis'
)


def layout():
    layout = dbc.Container([
        html.Div([
            html.H5("Attention Analysis",
                    className='mt-2 text-center'),
        ]),
        dbc.Tabs([
            dbc.Tab(label='prepared', tab_id='prepared-ana', children=tab_1),
            dbc.Tab(label='custom', tab_id='custom-ana', children=tab_2),
        ],
            active_tab="prepared-ana",
        ),
    ], fluid=True)
    return layout
