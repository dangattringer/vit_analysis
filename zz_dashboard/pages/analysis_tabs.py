import dash
import dash_bootstrap_components as dbc
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State
from lib.params import MODELS_DICT
from lib.utils import parse_contents, save_file

from .utils import (start_analysis, gen_model_arch_selection,
                    gen_selected_param_output, update_selected_parameters)

tab_1 = [
    dbc.Row([
        dbc.Col([
            dcc.Store(id='model-store-ana-t1'),
            gen_model_arch_selection(tab_id="ana-t1"),
            gen_selected_param_output(tab_id="ana-t1"),
            dbc.Button('Start Analysis',
                       id='start-button-t1', n_clicks=0),
            dcc.Loading(id="ls-loading-1",
                        children=[html.Div(id="ls-loading-output-t1")], type="default"),
            html.Div(id='start-analysis-t1'),
        ], width=2, className='ml-0 mr-0'),
    ]),
]


@callback(
    # Store the image paths in the store component
    Output('model-store-ana-t1', 'data'),
    Output('model-display-ana-t1', 'children'),
    Output('arch-display-ana-t1', 'children'),
    [Input('model-select-ana-t1', 'value'),
     Input('arch-select-ana-t1', 'value'),
     State('model-store-ana-t1', 'data')]
)
def update_selected_parameters_ana_t1(model, arch, state):
    return update_selected_parameters(model, arch, state)


@callback(
    Output('start-analysis-t1', 'children'),
    Output("ls-loading-output-t1", "children"),
    Output("start-button-t1", "n_clicks"),
    [Input('model-select-ana-t1', 'value'),
     Input('arch-select-ana-t1', 'value'),
     Input('start-button-t1', 'n_clicks')
     ],
    running=[
        (Output("start-button-t1", "disabled"), True, False),
    ],
)
def start_analysis_t1(model, arch, btn):
    return start_analysis(model=model, arch=arch, btn=btn, root="assets")


tab_2 = [
    dbc.Row([
        dbc.Col([
            dcc.Store(id='model-store-ana-t2'),
            gen_model_arch_selection(tab_id="ana-t2"),
            gen_selected_param_output(tab_id="ana-t2"),
            dbc.Button('Start Analysis',
                       id='start-button-t2', n_clicks=0),
            dcc.Loading(id="ls-loading-2",
                        children=[html.Div(id="ls-loading-output-t2")], type="default"),
            html.Div(id='start-analysis-t2'),
        ], width=2, className='ml-0 mr-0'),
        dbc.Col([
            dcc.Upload(
                id='upload-image-t2',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                multiple=False
            ),
            html.Div(id='output-image-upload-t2'),
        ],
            width=4,
            className='ml-0 mr-0'),
    ]),
]


@callback(
    Output('output-image-upload-t2', 'children'),
    Input('upload-image-t2', 'contents'),
    State('upload-image-t2', 'filename'))
def update_output(img, name):
    if img:
        children = [
            parse_contents(img, name)
        ]
        save_file(name, img)
        return children
    return dash.no_update


@callback(
    # Store the image paths in the store component
    Output('model-store-ana-t2', 'data'),
    Output('model-display-ana-t2', 'children'),
    Output('arch-display-ana-t2', 'children'),
    [Input('model-select-ana-t2', 'value'),
     Input('arch-select-ana-t2', 'value'),
     State('model-store-ana-t2', 'data')]
)
def update_selected_parameters_ana_t2(model, arch, state):
    return update_selected_parameters(model, arch, state)


@callback(
    Output('start-analysis-t2', 'children'),
    Output("ls-loading-output-t2", "children"),
    Output("start-button-t2", "n_clicks"),
    [Input('model-select-ana-t2', 'value'),
     Input('arch-select-ana-t2', 'value'),
     Input('start-button-t2', 'n_clicks'),
     Input('upload-image-t2', 'filename'),
     ],
    running=[
        (Output("start-button-t2", "disabled"), True, False),
    ],
)
def start_analysis_t2(model, arch, btn, img_filename):
    return start_analysis(model=model, arch=arch, btn=btn, root="upload", img_filename=img_filename)
