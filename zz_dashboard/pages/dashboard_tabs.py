import os
import os.path as osp

import dash
import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import callback, dcc, html
from dash.dependencies import Input, Output, State
from lib.params import MODELS_VALUES, UPLOAD_DIRECTORY
from lib.utils import get_img_paths, load_img_base64, parse_contents

from .utils import (gen_btn_next_prev, gen_model_arch_selection,
                    gen_selected_param_output, update_carousel_image_paths,
                    update_selected_parameters)

tab_1 = [
    dbc.Row([
        dbc.Col([
            gen_model_arch_selection(tab_id="t1"),
            gen_btn_next_prev(tab_id="t1"),
            daq.BooleanSwitch(
                id='toggle-switch-t1',
                label='Hide first 6 layers',
                on=False
            ),
            html.Abbr("\u003F",
                      title="The firs 6 layers of the models MAE-CT, MAE-CT-AUG"),
            
            gen_selected_param_output("t1"),
            dcc.Store(id='model-store-t1'),

        ], width=2, className='ml-0 mr-0'),
        dbc.Col([
                html.H5("Image", className='mt-2 text-center'),
                html.Hr(className="my-2"),
                dbc.Carousel(
                    id="carousel-t1",
                    items=get_img_paths(),
                    controls=True,
                    indicators=True,
                ),
                dcc.Store(id='image-store-t1')  # Store the image paths
                ], width=4, className='ml-0 mr-0',),
        dbc.Col([
            dbc.Row([
                html.Div(id='out-image-t1'),
            ]),
        ], width=5, className='ml-0 mr-0'),
    ]),
]


@callback(
    # Store the image paths in the store component
    Output('model-store-t1', 'data'),
    Output('model-display-t1', 'children'),
    Output('arch-display-t1', 'children'),
    [Input('model-select-t1', 'value'),
     Input('arch-select-t1', 'value'),
     Input('btn-next-t1', 'n_clicks'),
     Input('btn-previous-t1', 'n_clicks'),
     State('model-store-t1', 'data')]
)
def update_selected_parameters_t1(model, arch, next_clicks, prev_clicks, state):
    return update_selected_parameters(model, arch, next_clicks, prev_clicks, state)


@callback(
    # Store the image paths in the store component
    Output('image-store-t1', 'data'),
    [Input('model-select-t1', 'value'),
     Input('arch-select-t1', 'value'),
     Input('btn-next-t1', 'n_clicks'),
     Input('btn-previous-t1', 'n_clicks'),
     State('model-store-t1', 'data')]
)
def update_image_paths_t1(model, arch, next_clicks, prev_clicks, state):
    return update_carousel_image_paths(model, arch, next_clicks, prev_clicks, state)


# Update the buttons with the current state
@callback(
    [Output('btn-next-t1', 'n_clicks'),
     Output('btn-previous-t1', 'n_clicks')],
    [Input('model-select-t1', 'value')]
)
def update_button_state_t1(model):
    if model:
        index = MODELS_VALUES.index(model)
        return index, 0
    else:
        return dash.no_update


@callback(
    Output('out-image-t1', 'children'),
    [Input('image-store-t1', 'data'),  # Retrieve the image paths from the store
     Input('carousel-t1', 'active_index'),
     Input('toggle-switch-t1', 'on')]
)
def update_image_out_t1(image_paths, active_index, toggle_value):
    if image_paths:
        if active_index is None:
            active_index = 0
        path = image_paths[active_index]
        if not osp.exists(path):
            return html.Div([
            dbc.Alert(["The image for this model is not available yet. Please run the analysis first.",
                      html.Div(dcc.Link(dash.page_registry['pages.analysis']['path'],
                                        href=dash.page_registry['pages.analysis']['path']))],
                      color="warning", dismissable=True),
        ])
        img = load_img_base64(path, toggle_value)
        return parse_contents(img,
                              "CLS token attention maps for all heads and all layers")
    else:
        return dash.no_update


tab_2 = [
    dbc.Row([
        dbc.Col([
            gen_model_arch_selection(tab_id="t2"),
            gen_btn_next_prev(tab_id="t2"),
            daq.BooleanSwitch(
                id='toggle-switch-t2',
                label='Hide first 6 layers',
                on=False
            ),

            gen_selected_param_output(tab_id="t2"),
            dcc.Store(id='model-store-t2')

        ], width=2, className='ml-0 mr-0'),
        dbc.Col([
                html.Div(id='out-carousel-t2'),
                dbc.Carousel(
                    id="carousel-t2",
                    items=get_img_paths("upload"),
                    controls=True,
                    indicators=True,
                ),
                dcc.Store(id='image-store-t2')  # Store the image paths
                ], width=4, className='ml-0 mr-0',),
        dbc.Col([
            dbc.Row([
                html.Div(id='out-image-t2'),
            ]),
        ],
            width=5,
            className='ml-0 mr-0'),
    ]),
]


@callback(
    Output('out-carousel-t2', 'children'),
    [Input('model-select-t2', 'value'),]
)
def check_upload_img(model):
    if not os.listdir(UPLOAD_DIRECTORY):
        return html.Div([
            dbc.Alert(["No images uploaded yet. Please upload images and run the custom analysis at:",
                      html.Div(dcc.Link(dash.page_registry['pages.analysis']['path'],
                                        href=dash.page_registry['pages.analysis']['path']))],
                      color="warning", dismissable=True),
        ])
    else:
        return html.Div([
            html.H5("Image", className='mt-2 text-center'),
            html.Hr(className="my-2"),
            dbc.Carousel(
                id="carousel-t2",
                items=get_img_paths("upload"),
                controls=True,
                indicators=True,
            ),
        ])


@callback(
    # Store the image paths in the store component
    Output('model-store-t2', 'data'),
    Output('model-display-t2', 'children'),
    Output('arch-display-t2', 'children'),
    [Input('model-select-t2', 'value'),
     Input('arch-select-t2', 'value'),
     Input('btn-next-t1', 'n_clicks'),
     Input('btn-previous-t1', 'n_clicks'),
     State('model-store-t2', 'data')]
)
def update_selected_parameters_t2(model, arch, next_clicks, prev_clicks, state):
    return update_selected_parameters(model, arch, next_clicks, prev_clicks, state)


@callback(
    # Store the image paths in the store component
    Output('image-store-t2', 'data'),
    [Input('model-select-t2', 'value'),
     Input('arch-select-t2', 'value'),
     Input('btn-next-t2', 'n_clicks'),
     Input('btn-previous-t2', 'n_clicks'),
     State('model-store-t2', 'data')]
)
def update_image_paths_t2(model, arch, next_clicks, prev_clicks, state):
    return update_carousel_image_paths(model, arch, next_clicks, prev_clicks, state, root="upload")


# Update the buttons with the current state
@callback(
    [Output('btn-next-t2', 'n_clicks'),
     Output('btn-previous-t2', 'n_clicks')],
    [Input('model-select-t2', 'value')]
)
def update_button_state_t2(model):
    if model:
        index = MODELS_VALUES.index(model)
        return index, 0
    else:
        return dash.no_update


@callback(
    Output('out-image-t2', 'children'),
    [Input('image-store-t2', 'data'),  # Retrieve the image paths from the store
     Input('carousel-t2', 'active_index'),
     Input('toggle-switch-t2', 'on')]
)
def update_image_out_t2(image_paths, active_index, toggle_value):
    if image_paths:
        if active_index is None:
            active_index = 0
        path = image_paths[active_index]
        img = load_img_base64(path, toggle_value)
        return parse_contents(img,
                              "CLS token attention maps for all heads and all layers")
    else:
        return dash.no_update
