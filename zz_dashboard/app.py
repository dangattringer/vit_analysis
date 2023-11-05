import argparse
import os
import os.path as osp
import sys
from glob import glob

import dash
import dash_bootstrap_components as dbc
from dash import Dash, html
from lib.params import UPLOAD_DIRECTORY, CWD
from navigation import navigation_bar

sys.path.append(osp.dirname(CWD))

def clean_upload_folder():
    if osp.exists(UPLOAD_DIRECTORY):
        for file in glob(osp.join(UPLOAD_DIRECTORY, "*")):
            os.remove(file)
    else:
        os.makedirs(UPLOAD_DIRECTORY)

# parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='127.0.0.1', type=str)
    parser.add_argument('--port', default=8050, type=int)
    parser.add_argument('--debug', default=False, action='store_true')
    return parser.parse_args()


if __name__ == '__main__':
    clean_upload_folder()

    app = Dash(__name__,
        suppress_callback_exceptions=True,
        external_stylesheets=[dbc.themes.FLATLY],
        use_pages=True,
        )

    app.layout = html.Div([
        navigation_bar,
        dash.page_container
    ])


    # Create server variable with Flask server object for use with gunicorn
    server = app.server
    args = parse_args()
    app.run_server(host=args.host, port=args.port, debug=args.debug)
