import os
import os.path as osp
from glob import glob
from base64 import b64encode


CWD = os.getcwd()
CWD_PARENT = osp.dirname(CWD)
MODELS = [{"label": "MAE-ViT", "value": "mae"},
          {"label": "MAE-CT", "value": "mae_ct"},
          {"label": "MAE-CT-AUG", "value": "mae_ct_aug"},
          {"label": "MAE-REIMPL", "value": "mae_reimpl"}]
MODELS_VALUES = [model['value'] for model in MODELS]
MODELS_LABELS = [model['label'] for model in MODELS]
MODELS_DICT = {model['value']: model['label'] for model in MODELS}
ARCHS = ["B", "L", "H"]

IMAGES = [{"key": img, "src": f"data:image/jpg;base64,{b64encode(open(img, 'rb').read()).decode()}"} for img in glob(
    './assets/*')]

UPLOAD_DIRECTORY = os.path.join(os.getcwd(), "upload")
