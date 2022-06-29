# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.9.1
#   kernelspec:
#     display_name: Python [conda env:sophie] *
#     language: python
#     name: conda-env-sophie-py
# ---

# # Template

# %load_ext autoreload
# %load_ext rpy2.ipython
# %autoreload 2
import os
from ponyo import utils, train_vae_modules
from sophie import process

# Set seeds to get reproducible VAE trained models
train_vae_modules.set_all_seeds()

# +
# Read in config variables
config_filename = "config_example.tsv"

params = utils.read_config(config_filename)

# +
# Load config params

# Local directory to store intermediate files
local_dir = params["local_dir"]

# Raw compendium filename
raw_compendium_filename = params["raw_compendium_filename"]

# Normalized compendium filename
normalized_compendium_filename = params["normalized_compendium_filename"]
# -

# ## Setup directories

utils.setup_dir(config_filename)

# ## Normalize compendium
#
# Normalization is required to ensure that the distribution of features are similar, which will otherwise cause difficulty in training. Additionally, normalization is required to produce values in the 0-1 range, which is needed since the VAE model is using a cross-entropy loss function.

train_vae_modules.normalize_expression_data(
    config_filename,
    raw_compendium_filename,
    normalized_compendium_filename)

# ## Train VAE
#
# Optimal parameters for training the VAE must be manually selected by the user. For some guidance, please refer to some example configurations that sucessfully trained in [simulate-expression-compendia](https://github.com/greenelab/simulate-expression-compendia/tree/master/configs) and [generic-expression-patterns](https://github.com/greenelab/generic-expression-patterns/tree/master/configs) repositories.
#
# Also see discussions in the following issues:
# * https://github.com/greenelab/generic-expression-patterns/issues/109
# * https://github.com/greenelab/generic-expression-patterns/issues/116

# Train VAE
train_vae_modules.train_vae(config_filename,
                            normalized_compendium_filename)
