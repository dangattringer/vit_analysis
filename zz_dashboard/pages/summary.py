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


# def layout():
#     layout = dbc.Container([
#         html.Div([
#             html.H5("Attention Analysis",
#                     className='mt-2 text-center'),
#         ]),
#         dbc.Row([
#             dbc.Col([
#                 html.H5("Model",
#                         className='mt-2'),
#                 html.Hr(className="my-2"),
#                 dcc.Checklist(
#                     MODELS,
#                     id='model-select-sum',
#                     style={"display": "flex", "flex-direction": "row",
#                            "column-gap": "14px"},
#                     labelStyle={"display": "flex",
#                                 "gap": "4px", "align-items": "center"},
#                 ),
#                 html.H5("Architecture",
#                         className='mt-2'),
#                 html.Hr(className="my-2"),
#                 dcc.RadioItems(
#                     ARCHS,
#                     id='arch-select-sum',
#                     style={"display": "flex", "flex-direction": "row",
#                            "column-gap": "14px"},
#                     labelStyle={"display": "flex",
#                                 "gap": "4px", "align-items": "center"},
#                 ),
#                 html.Hr(className="my-2"),
#                 dcc.Checklist(
#                     options=[
#                         {"label": "Add Scatter Plot", "value": "add_scatter"},
#                         {"label": "Add Line Plot", "value": "add_line"},
#                         {"label": "Separate Plots", "value": "separate_plots"},
#                     ],
#                     value=["add_scatter", "add_line"],
#                     id='plot-options-sum',
#                     style={"display": "flex", "flex-direction": "column",
#                            "column-gap": "14px"},
#                     labelStyle={"display": "flex",
#                                 "gap": "4px", "align-items": "center"},
#                 ),
#                 html.Button("Download", id="btn-image", n_clicks=0),
#             ], className='ml-0 mr-0'),
#         ]),
#         dbc.Row([
#             dbc.Col([
#                 html.Div(id='graph-sum'),
#                 dcc.Download(id="download-image"),
#             ], width=12, className='ml-0 mr-0'),
#         ]),
#     ], fluid=True)
#     return layout


# @callback(
#     Output("download-image", "data"),
#     Output("btn-image", "n_clicks"),
#     [Input("btn-image", "n_clicks"),
#      Input('graph-sum', 'children'),
#      Input('model-select-sum', 'value'),
#      Input('arch-select-sum', 'value'),
#      Input('plot-options-sum', 'value')],
#     prevent_initial_call=True,
# )
# def download_img_sum(n_clicks, graph_children, model, arch, plot_options):
#     if graph_children and n_clicks > 0:
#         img_format = 'png'
#         graph_figure = graph_children['props']['figure']
#         title = graph_children["props"]['figure']['layout']['title']['text']
#         title = title.replace(" ", "-")
#         model = [MODELS_DICT[m] for m in model]
#         # add options to filename
#         fname_options = [title, arch]
#         fname_options.extend(model)
#         if 'add_scatter' in plot_options:
#             fname_options.append('scatter')
#         if 'add_line' in plot_options:
#             fname_options.append('line')
#         if 'separate_plots' in plot_options:
#             fname_options.append('separate')
#         filename = '-'.join(fname_options) + f'.{img_format}'
#         image_data = pio.to_image(graph_figure, format=img_format)
#         download_data = io.BytesIO(image_data)
#         return dcc.send_bytes(src=download_data.getvalue(), filename=filename), 0

#     return dash.no_update


# @callback(
#     Output('graph-sum', 'children'),
#     [Input('model-select-sum', 'value'),
#      Input('arch-select-sum', 'value'),
#      Input('plot-options-sum', 'value'),])
# def gen_plots_sum(model, arch, plot_options):
#     if model and arch:
#         if isinstance(model, str):
#             model = [model]
#         kwargs = {option: True for option in plot_options}
#         fig = gen_plots(model, arch, **kwargs)
#         return dcc.Graph(figure=fig)
#     else:
#         return dash.no_update


# @callback(
#     # Store the image paths in the store component
#     Output('model-display-sum', 'children'),
#     Output('arch-display-sum', 'children'),
#     Output('scatter-display-sum', 'children'),
#     Output('line-display-sum', 'children'),
#     Output('seperate-plots-display-sum', 'children'),
#     [Input('model-select-sum', 'value'),
#      Input('arch-select-sum', 'value'),
#      Input('plot-options-sum', 'value')]
# )
# def update_selected_parameters_sum(model, arch, plot_options):
#     if isinstance(model, list):
#         model = [MODELS_DICT[m] for m in model]
#         curr_model = " & ".join(model)
#     else:
#         curr_model = model
#     scatter = 'Yes' if 'add_scatter' in plot_options else 'No'
#     line = 'Yes' if 'add_line' in plot_options else 'No'
#     seperate = 'Yes' if 'separate_plots' in plot_options else 'No'
#     return (f"Current Model: {curr_model}",
#             f"Current Architecture: {arch}",
#             f"Scatter Plot: {scatter}",
#             f"Line Plot: {line}",
#             f"Seperate Plots: {seperate}")
