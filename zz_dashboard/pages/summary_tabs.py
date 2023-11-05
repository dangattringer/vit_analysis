import os.path as osp

import dash
import dash_bootstrap_components as dbc
from dash import callback, dcc, html
from dash.dependencies import Input, Output
from lib.params import ARCHS, MODELS
from lib.utils import load_img_base64, parse_contents

from meta_utils.get_model_wrapper import get_model_wrapper

from .utils import download_img, gen_args, gen_plots

tab_1 = [
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H5("Model",
                        className='mt-2'),
                html.Hr(className="my-2"),
                dcc.Checklist(
                    MODELS,
                    id='model-select-sum-t1',
                    style={"display": "flex", "flex-direction": "row",
                           "column-gap": "14px"},
                    labelStyle={"display": "flex",
                                "gap": "4px", "align-items": "center"},
                ),
                html.H5("Architecture",
                        className='mt-2'),
                html.Hr(className="my-2"),
                dcc.RadioItems(
                    ARCHS,
                    id='arch-select-sum-t1',
                    style={"display": "flex", "flex-direction": "row",
                           "column-gap": "14px"},
                    labelStyle={"display": "flex",
                                "gap": "4px", "align-items": "center"},
                ),
                html.Hr(className="my-2"),
                dcc.Checklist(
                    options=[
                        {"label": "Add Scatter Plot", "value": "add_scatter"},
                        {"label": "Add Line Plot", "value": "add_line"},
                        {"label": "Separate Plots",
                         "value": "separate_plots"},
                    ],
                    value=["add_scatter", "add_line"],
                    id='plot-options-sum-t1',
                    style={"display": "flex", "flex-direction": "column",
                           "column-gap": "14px"},
                    labelStyle={"display": "flex",
                                "gap": "4px", "align-items": "center"},
                ),
            ], className='ml-0 mr-0'),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(id="btn-image-sum-t1"),
                dcc.Download(id="download-image-sum-t1"),
                html.Div(id='graph-sum-t1'),
            ], width=12, className='ml-0 mr-0'),
        ]),
    ], fluid=True)
]


@callback(
    Output("download-image-sum-t1", "data"),
    Output("btn-image-sum-t1", "n_clicks"),
    [Input("btn-image-sum-t1", "n_clicks"),
     Input('graph-sum-t1', 'children'),
     Input('model-select-sum-t1', 'value'),
     Input('arch-select-sum-t1', 'value'),
     Input('plot-options-sum-t1', 'value')],
    prevent_initial_call=True,
)
def download_img_sum_t1(n_clicks, graph_children, model, arch, plot_options):
    return download_img(n_clicks, graph_children, model, arch, plot_options)


@callback(
    Output('graph-sum-t1', 'children'),
    [Input('model-select-sum-t1', 'value'),
     Input('arch-select-sum-t1', 'value'),
     Input('plot-options-sum-t1', 'value'),])
def gen_plots_sum_t1(model, arch, plot_options):
    if model and arch:
        if isinstance(model, str):
            model = [model]
        kwargs = {option: True for option in plot_options}
        fig = gen_plots(model, arch, **kwargs)
        return dcc.Graph(figure=fig)
    else:
        return dash.no_update


@callback(
    Output('btn-image-sum-t1', 'children'),
    [Input('graph-sum-t1', 'children')])
def download_btn_sum_t1(graph):
    if graph:
        return html.Button("Download", n_clicks=0)
    else:
        return dash.no_update


tab_2 = [
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H5("Model",
                        className='mt-2'),
                html.Hr(className="my-2"),
                dcc.RadioItems(
                    MODELS,
                    id='model-select-sum-t2',
                    style={"display": "flex", "flex-direction": "row",
                           "column-gap": "14px"},
                    labelStyle={"display": "flex",
                                "gap": "4px", "align-items": "center"},
                ),
                html.H5("Architecture",
                        className='mt-2'),
                html.Hr(className="my-2"),
                dcc.RadioItems(
                    ARCHS,
                    id='arch-select-sum-t2',
                    style={"display": "flex", "flex-direction": "row",
                           "column-gap": "14px"},
                    labelStyle={"display": "flex",
                                "gap": "4px", "align-items": "center"},
                ),
                html.Hr(className="my-2"),
            ], className='ml-0 mr-0'),
        ]),
        dbc.Row([
            dbc.Col([
                html.Div(id="btn-image-sum-t2"),
                dcc.Download(id="download-image-sum-t2"),
                html.Div(id='out-image-sum-t2'),
            ], width=12, className='ml-0 mr-0'),
        ]),
    ], fluid=True)
]


@callback(
    Output("download-image-sum-t2", "data"),
    Output("btn-image-sum-t2", "n_clicks"),
    [Input("btn-image-sum-t2", "n_clicks"),
     Input('out-image-sum-t2', 'children'),
     Input('model-select-sum-t2', 'value'),
     Input('arch-select-sum-t2', 'value')
     ],
    prevent_initial_call=True,
)
def download_img_sum_t2(n_clicks, graph_children, model, arch):
    return download_img(n_clicks, graph_children, model, arch, None)


def load_maps(model, arch):
    if model and arch:
        args = gen_args(model, arch)
        mod_id = get_model_wrapper(
            args.meta_model, args.arch, args.patch, args.imsize, 'attn').mod_id
        path = osp.join(args.output_dir, mod_id,
                        f"{mod_id}_tokenplot_avg-cls-att-on-token-[PRE-SCALED].png")
        img = load_img_base64(path)
        return parse_contents(img, "", width=50, height=50)
    else:
        return dash.no_update


@callback(
    Output('out-image-sum-t2', 'children'),
    [Input('model-select-sum-t2', 'value'),
     Input('arch-select-sum-t2', 'value'),
     ])
def gen_plots_sum_t2(model, arch):
    if model and arch:
        return load_maps(model, arch)
    else:
        return dash.no_update


@callback(
    Output('btn-image-sum-t2', 'children'),
    [Input('out-image-sum-t2', 'children')])
def download_btn_sum_t2(graph):
    if graph:
        return html.Button("Download", n_clicks=0)
    else:
        return dash.no_update
