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
base_dir = os.path.abspath(os.path.join(os.getcwd(), "../"))

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

# ## Make directories

# +
# TO DO: Add with new ponyo version
# -

# ## Normalize compendium

"""train_vae_modules.normalize_expression_data(
    base_dir, ## TO DO: remove after update
    config_filename,
    raw_compendium_filename,
    normalized_compendium_filename)
"""
## TO DO: change to scaler_filename with new version

# ## Train VAE

# +
## TO DO: REMOVE with new ponyo version
# Create VAE directories if needed

# REMOVE LATER
NN_architecture = "NN_test"
dataset_name = "new_model_seen_template"

output_dirs = [
    os.path.join(base_dir, dataset_name, "models"),
    os.path.join(base_dir, dataset_name, "logs"),
]

# Check if NN architecture directory exist otherwise create
for each_dir in output_dirs:
    sub_dir = os.path.join(each_dir, NN_architecture)
    os.makedirs(sub_dir, exist_ok=True)
# -

# Train VAE on new compendium data
train_vae_modules.train_vae(config_filename, normalized_compendium_filename)
