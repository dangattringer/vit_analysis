import io
import os.path as osp
from base64 import b64encode, decodebytes
from glob import glob

from dash import html
from lib.params import CWD, MODELS, UPLOAD_DIRECTORY
from PIL import Image


def get_img_paths(path="assets"):
    return [{"key": img, "src": f"data:image/jpg;base64,{b64encode(open(img, 'rb').read()).decode()}"} for img in glob(
        osp.join(CWD, path, '*'))]


def load_img_base64(img_path, toggle_value=False):
    with open(img_path, "rb") as img_file:
        string = img_file.read()

    if toggle_value:
        img = Image.open(io.BytesIO(string))
        width, height = img.size
        crop = img.crop((0, 6 * height / 12, width, height))
        buffered = io.BytesIO()
        crop.save(buffered, format=img.format)
        string = buffered.getvalue()

    encoded_string = b64encode(string)
    return f"data:image/png;base64,{encoded_string.decode()}"


def calc_model_index(next_clicks, prev_clicks, triggered_button):
    if triggered_button == 'next' and next_clicks:
        combined_clicks = next_clicks - prev_clicks
    elif triggered_button == 'previous' and prev_clicks:
        combined_clicks = -(prev_clicks - next_clicks)
    else:
        return None

    name_index = combined_clicks % len(MODELS)
    return MODELS[name_index]['value']


def parse_contents(contents, caption, width=100, height=100):
    return html.Div([
        html.H5(caption,
                className='mt-2 text-center'),
        html.Hr(className="my-2"),
        html.Img(src=contents,
                 width=f"{width}%",
                 height=f"{height}%"),
    ])


def save_file(name, content):
    data = content.encode("utf8").split(b";base64,")[1]
    with open(osp.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(decodebytes(data))
