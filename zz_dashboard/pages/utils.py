import argparse
import io
import math
import os.path as osp
from base64 import decodebytes

import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
from dash import dcc, html
from lib.params import ARCHS, CWD, CWD_PARENT, MODELS, MODELS_DICT
from lib.utils import calc_model_index, get_img_paths
from plotly.subplots import make_subplots

from analysis.attention_plots import get_line_fmt
from meta_utils.get_model_wrapper import get_model_wrapper
from run_attention_analysis import (export_attention_maps,
                                    load_or_run_analysis, make_attention_grids,
                                    run_metrics)


def gen_model_arch_selection(tab_id):
    return html.Div([
        html.H5("Model",
                className='mt-2 text-center'),
        html.Hr(className="my-2"),
        dcc.Dropdown(
            id=f'model-select-{tab_id}',
            multi=False,
            placeholder='Select Model...',
            options=MODELS,
            searchable=True,
            clearable=False,
            persistence=False,
        ),
        html.H5("Architecture",
                className='mt-2 text-center'),
        html.Hr(className="my-2"),
        dcc.Dropdown(
            id=f'arch-select-{tab_id}',
            multi=False,
            placeholder='Select Architecture...',
            options=ARCHS,
            searchable=True,
            clearable=False,
            persistence=False,
        ),
        html.Hr(className="my-2")
    ])


def gen_selected_param_output(tab_id):
    return html.Div([
        html.H5('Selected Parameters', className='mt-2 text-center'),
        html.P(id=f'model-display-{tab_id}', style={'font-size': '14px'}),
        html.P(id=f'arch-display-{tab_id}', style={'font-size': '14px'})
    ])


def gen_btn_next_prev(tab_id):
    return html.Div([
        dbc.Button('Previous', id=f'btn-previous-{tab_id}', n_clicks=0,
                   outline=True, color="primary",
                   style={"verticalAlign": "middle"}),
        dbc.Button('Next', id=f'btn-next-{tab_id}', n_clicks=0,
                   outline=True, color="primary",
                   style={"verticalAlign": "middle", }),
    ], className="d-grid gap-2",)


def check_exists(args, img_filename):
    mod_wrap = get_model_wrapper(
        args.meta_model, args.arch, args.patch, args.imsize, 'attn')
    mod_id = mod_wrap.mod_id
    if not img_filename:
        out = osp.join(args.vis_out, mod_id, "head-v-pos")
    else:
        out = osp.join(args.vis_out, mod_id, img_filename)
    return osp.exists(out)


def load_heads_image(model, arch, img):
    model = MODELS_DICT[model]
    return osp.join(CWD, "analysis", "vis_out", f"{model}-{arch}-16-224", "head-v-pos",
                    f"{model}-{arch}-16-224_(img {img})_(blk YAXIS)_(pos cls)_(head XAXIS).png")


def get_model_from_btn(model, next_clicks, prev_clicks, state):
    ctx = dash.callback_context
    prop_id = ctx.triggered_id
    action = prop_id.split('-')[0] if prop_id else prop_id
    if state and not model:
        model = state
    if action == 'btn':
        triggered_button = prop_id.split('-')[1]
        model = calc_model_index(next_clicks, prev_clicks, triggered_button)
    return model


def update_carousel_image_paths(model, arch, next_clicks, prev_clicks, state, root="assets"):
    model = get_model_from_btn(model, next_clicks, prev_clicks, state)
    if model and arch:
        image_paths = []
        for item in get_img_paths(root):
            img = osp.basename(item["key"])
            path = load_heads_image(model, arch, img)
            image_paths.append(path)
        return image_paths
    else:
        return []


def update_selected_parameters(model, arch, next_clicks=None, prev_clicks=None, state=None):
    model = get_model_from_btn(model, next_clicks, prev_clicks, state)
    return (model,
            f"Current Model: {MODELS_DICT[model] if model else model}",
            f"Current Architecture: {arch}")


def gen_args(model, arch, *, patch=16, imsize=224, nocache=False, overcache=False,
             perclass=100, batch=2, root="assets", img_filename=None):
    args = argparse.Namespace()
    args.meta_model = model
    args.arch = arch
    args.patch = patch
    args.imsize = imsize
    args.nocache = nocache
    args.overcache = overcache
    args.dataroot = osp.join(CWD_PARENT, "data", "img50")
    args.perclass = perclass
    args.batch = batch
    args.output_dir = osp.join(CWD, "analysis", "attention_analysis_out")
    args.vis_dump = osp.join(CWD, "analysis", "vis_dump")
    args.vis_in = osp.join(
        CWD, root,  img_filename) if img_filename else osp.join(CWD, root)
    args.vis_out = osp.join(CWD, "analysis", "vis_out")
    return args


def start_analysis(model, arch, btn, root, img_filename=None):
    if btn >= 1 and model and arch:
        args = gen_args(model, arch, root=root, img_filename=img_filename)
        if (root == "assets" or img_filename) and not check_exists(args, img_filename):
                export_attention_maps(args=args, just_cls=True)
                make_attention_grids(args, just_cls=True)
                return html.P("Analysis Completed",
                            className='mt-2 text-center'), dash.no_update, 0
        else:
            return html.P("Found Exisiting Analysis (cached)",
                          className='mt-2 text-center'), dash.no_update, 0
    else:
        return dash.no_update


def gen_plots(models, arch, **kwargs):
    add_scatter = kwargs.get('add_scatter', False)
    add_line = kwargs.get('add_line', False)
    separate_plots = kwargs.get('separate_plots', False)
    figs = []
    for model in models:
        if model == "mae" and arch == "H":
            continue
        fig = go.Figure()
        args = gen_args(model, arch)
        mod_id = get_model_wrapper(
            args.meta_model, args.arch, args.patch, args.imsize, 'attn').mod_id
        analysis_methods = ['avg-att-dist']
        all_img_res = load_or_run_analysis(args, analysis_methods)[
            analysis_methods[0]]
        m = np.mean(all_img_res, axis=0)
        x = np.arange(0, all_img_res.shape[2])

        mp = np.mean(m, axis=1)
        x = np.arange(0, mp.shape[0])
        tmp_mod_id = mod_id.split('-')
        if tmp_mod_id[1] in ["CT", "REIMPL"]:
            tmp_mod_id = mod_id.rsplit('-', 3)[0]
        else:
            tmp_mod_id = tmp_mod_id[0]

        reduce_sat = 0.75
        col, mrk, lst = get_line_fmt(tmp_mod_id,
                                     reduce_sat=reduce_sat,
                                     px=True)
        if reduce_sat < 1:
            col = [x * 255 for x in col]
            col = f'rgb{tuple(col)}'
        if add_line:
            fig.add_trace(go.Scatter(x=x, y=mp,
                                     name=tmp_mod_id,
                                     marker=dict(size=15,
                                                 symbol=mrk,
                                                 color=col),
                                     line=dict(color=col, dash=lst)))
        if add_scatter:
            for b in range(m.shape[1]):
                y_m = m[:, b]
                fig.add_trace(go.Scatter(x=x, y=y_m,
                                         showlegend=False,
                                         name=tmp_mod_id,
                                         mode='markers',
                                         marker=dict(symbol=mrk, color=col)))
        figs.append(fig)
    if separate_plots:
        num_rows = int(math.ceil(len(figs) / 2))
        num_cols = min(len(figs), 2)
        fig = make_subplots(rows=num_rows, cols=num_cols,
                            shared_xaxes=True, shared_yaxes=True,
                            horizontal_spacing=0, vertical_spacing=0,
                            x_title='Layer', y_title='Distance')
        for i, figure in enumerate(figs):
            row = (i // num_cols) + 1
            col = (i % num_cols) + 1
            if add_scatter and not add_line:
                figure.data[0].showlegend = True
            for trace in figure.data:
                fig.add_trace(trace, row=row, col=col)

    else:
        fig = go.Figure(layout=dict(xaxis_title='Layer',
                                    yaxis_title='Distance',
                                    font=dict(size=13)))
        for figure in figs:
            if add_scatter and not add_line:
                figure.data[0].showlegend = True
            for trace in figure.data:
                fig.add_trace(trace)

    fig.update_layout(
        title=dict(text="Attention Distance",
                   font=dict(size=20),
                   xref='paper',
                   xanchor='center',
                   yanchor='middle',
                   x=0.5),
        showlegend=True,
        plot_bgcolor='white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    fig.update_xaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    fig.update_yaxes(
        mirror=True,
        ticks='outside',
        showline=True,
        linecolor='black',
        gridcolor='lightgrey'
    )
    return fig


def download_img(n_clicks, graph_children, model, arch, plot_options):
    if graph_children and n_clicks and n_clicks > 0:
        img_format = 'png'
        props = graph_children['props']
        if props.get('figure', None):
            graph_figure = props['figure']
            title = graph_figure['layout']['title']['text']
            title = title.replace(" ", "-")

            model = [MODELS_DICT[m] for m in model]
            fname_options = [title, arch]
            fname_options.extend(model)
            if 'add_scatter' in plot_options:
                fname_options.append('scatter')
            if 'add_line' in plot_options:
                fname_options.append('line')
            if 'separate_plots' in plot_options:
                fname_options.append('separate')
            filename = '-'.join(fname_options) + f'.{img_format}'
            image_data = pio.to_image(graph_figure, format=img_format)
        else:
            model = MODELS_DICT[model]
            graph_figure = props['children']
            image_data = graph_figure[2]['props']['src']
            image_data = image_data.encode("utf8").split(b";base64,")[1]
            image_data = decodebytes(image_data)
            filename = f"Attention-Maps-of-CLS-token-{model}.{img_format}"

        download_data = io.BytesIO(image_data)
        return dcc.send_bytes(src=download_data.getvalue(), filename=filename), 0

    return dash.no_update
