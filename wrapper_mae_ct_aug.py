"""
###########################################################################
Model wrapper for MAE ViTs to extract both attention and features.

Based partly on mea/demo/mae_visualize.ipynb from the original MAE repo:
https://github.com/facebookresearch/mae

Written by: Matthew Walmer
###########################################################################
"""
import sys
import os.path as osp

import torch

from meta_utils.feature_extractor import FeatureExtractor
from meta_utils.block_mapper import block_mapper
from meta_utils.preproc import standard_transform

path_dir = osp.dirname(__file__)
sys.path.append(osp.join(path_dir, "MAE-CT"))
from models.vit.masked_encoder import MaskedEncoder


class MAE_CT_AUG_Wrapper:
    def __init__(self, arch, patch, imsize, extract_mode='none', blk_sel='all'):
        assert extract_mode in ['none', 'attn', 'feat']
        if extract_mode == 'none':
            print('WARNING: wrapper running in NONE mode, no tensors will be extracted')
            print('only use this mode if extracting features separately')
        self.arch = arch
        self.patch = patch
        self.imsize = imsize
        self.extract_mode = extract_mode
        self.device = torch.device(
            "cuda") if torch.cuda.is_available() else torch.device("cpu")
        # create model identifier and test configuration
        if imsize != 224:
            print('ERROR: Required imsize for MAE is 224')
            exit(-1)
        self.mod_id = 'MAE-CT-AUG-%s-%i-%i' % (arch, patch, imsize)

        if self.mod_id == 'MAE-CT-AUG-B-16-224':
            self.checkpoint_file = osp.join(
                path_dir, 'models', 'mae_ct_aug', 'maectaug_base16.th')
        elif self.mod_id == 'MAE-CT-AUG-L-16-224':
            self.checkpoint_file = osp.join(
                path_dir, 'models', 'mae_ct_aug', 'maectaug_large16.th')
        elif self.mod_id == 'MAE-CT-AUG-H-16-224':
            self.checkpoint_file = osp.join(
                path_dir, 'models', 'mae_ct_aug', 'maectaug_large16.th')
        else:
            print('ERROR: Invalid MAE config')
            exit(-1)
        # prepare transform
        self.transform = standard_transform('mae', imsize)
        # handle block selection
        self.blk_sel = blk_sel
        self.blk_idxs = block_mapper(arch, blk_sel)

    def load(self):
        print(f"initialize encoder ({self.checkpoint_file})")
        encoder_sd = torch.load(self.checkpoint_file,
                                map_location=torch.device("cpu"))
        if "state_dict" in encoder_sd:
            encoder_sd = encoder_sd["state_dict"]
        embed_dim = encoder_sd["cls_token"].shape[2]
        patch_size = encoder_sd["patch_embed.proj.weight"].shape[2]
        if embed_dim == 768:
            depth = 12
            attention_heads = 12
        elif embed_dim == 1024:
            depth = 24
            attention_heads = 16
        elif embed_dim == 1280:
            depth = 32
            attention_heads = 16
        else:
            raise NotImplementedError
        self.model = MaskedEncoder(
            input_shape=(3, 224, 224),
            patch_size=patch_size,
            embedding_dim=embed_dim,
            depth=depth,
            attention_heads=attention_heads,
        )
        self.model.load_state_dict(encoder_sd)

        self.model = self.model.to(self.device)
        self.model.eval()
        # prepare hooks - depending on extract_mode
        layers = []
        for idx in self.blk_idxs:
            if self.extract_mode == 'none':
                continue
            if self.extract_mode == 'attn':
                layers.append(self.model.blocks[idx].attn.attn_drop)
            if self.extract_mode == 'feat':
                layers.append(self.model.blocks[idx])
        self.extractor = FeatureExtractor(self.model.features, layers)

    def get_activations(self, x):
        # , mask_ratio=0.0, no_shuffle=True
        acts = self.extractor(x.to(self.device))
        return acts
