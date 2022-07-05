"""
Author: Alexandra Lee
Date Created: 16 June 2020

This script provide supporting functions to run analysis notebooks.

Data processing functions including:
* function to map ensembl gene ids to hgnc symbols
* function to remove subsets of samples
* function to transform data into integer for downstream DE and GSEA analyses
* function to normalize data
* function to format pseudomonas pathway data to input to GSEA
"""

import os
import pickle
import random
import tensorflow as tf
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from glob import glob


from sklearn.preprocessing import MinMaxScaler
from ponyo import simulate_expression_data

# Setup function


def set_all_seeds(np_seed=42, rn_seed=12345, tf_seed=1234):
    """
    This function sets all seeds to get reproducible VAE trained
    models.
    """

    # The below is necessary in Python 3.2.3 onwards to
    # have reproducible behavior for certain hash-based operations.
    # See these references for further details:
    # https://keras.io/getting-started/faq/#how-can-i-obtain-reproducible-results-using-keras-during-development
    # https://docs.python.org/3.4/using/cmdline.html#envvar-PYTHONHASHSEED
    # https://github.com/keras-team/keras/issues/2280#issuecomment-306959926

    os.environ["PYTHONHASHSEED"] = "0"

    # The below is necessary for starting Numpy generated random numbers
    # in a well-defined initial state.
    np.random.seed(np_seed)

    # The below is necessary for starting core Python generated random numbers
    # in a well-defined state.
    random.seed(rn_seed)
    # The below tf.set_random_seed() will make random number generation
    # in the TensorFlow backend have a well-defined initial state.
    tf.set_random_seed(tf_seed)


def create_recount2_compendium(download_dir, output_filename):
    """
    Concatenate `t_data_counts.tsv` in each project directory and create the
    single recount2 commpendium file in TSV format.
    The first row in each `t_data_counts.tsv` is a header line that includes
    column names, so only the header in the first `t_data_counts.tsv` is copied
    to the output file.

    Arguments
    ---------
    download_dir: str
        dirname that hosts all downloaded projects data
    output_filename: str
        filename of output single compendium data
    """

    data_counts_filenames = glob(f"{download_dir}/*/t_data_counts.tsv")
    data_counts_filenames.sort()

    compendium_header = None
    with open(output_filename, "w") as ofh:
        for filename in data_counts_filenames:
            with open(filename) as ifh:
                file_header = ifh.readline()
                if compendium_header is None:
                    compendium_header = file_header
                    ofh.write(compendium_header)
                elif file_header != compendium_header:
                    raise Exception(f"Inconsistent header in {filename}")

                file_content = ifh.read()
                ofh.write(file_content)


def process_raw_template_pseudomonas(
    processed_compendium_filename,
    project_id,
    metadata_filename,
    metadata_delimiter,
    experiment_id_colname,
    sample_id_colname,
    raw_template_filename,
):
    """
    Create processed pseudomonas template data file based on
    processed compendium file (`compendium_filename`),
    drop sample rows if needed, and save updated
    template data on disk.
    """

    # Get sample ids associated with selected project id
    sample_ids = simulate_expression_data.get_sample_ids(
        metadata_filename,
        metadata_delimiter,
        experiment_id_colname,
        project_id,
        sample_id_colname,
    )

    # Get samples from experiment id
    processed_compendium = pd.read_csv(
        processed_compendium_filename, header=0, index_col=0, sep="\t"
    )
    template_data = processed_compendium.loc[sample_ids]

    template_data.to_csv(raw_template_filename, sep="\t")


def normalize_compendium(
    mapped_filename, normalized_filename, scaler_filename,
):
    """
    Read the mapped compendium file into memory, normalize it, and save
    both normalized compendium data and pickled scaler on disk.
    """

    # Read mapped compendium file: ~4 minutes (17 GB of RAM)
    mapped_compendium_df = pd.read_table(
        mapped_filename, header=0, sep="\t", index_col=0
    )
    print(
        "input: dataset contains {} samples and {} genes".format(
            mapped_compendium_df.shape[0], mapped_compendium_df.shape[1]
        )
    )

    # 0-1 normalize per gene
    scaler = MinMaxScaler()

    # Fitting (2 minutes, ~8 GB of RAM)
    normalized_compendium = scaler.fit_transform(mapped_compendium_df)
    normalized_compendium_df = pd.DataFrame(
        normalized_compendium,
        columns=mapped_compendium_df.columns,
        index=mapped_compendium_df.index,
    )

    # Save normalized data on disk: ~17.5 minutes
    normalized_compendium_df.to_csv(normalized_filename, float_format="%.3f", sep="\t")
    del normalized_compendium_df

    # Pickle `scaler` as `scaler_filename` on disk
    with open(scaler_filename, "wb") as pkl_fh:
        pickle.dump(scaler, pkl_fh, protocol=3)


def process_raw_compendium_pseudomonas(
    raw_filename, processed_filename, normalized_filename, scaler_filename,
):
    """
    Create processed pseudomonas compendium data file based on raw compendium
    data file (`raw_filename`), and normalize the processed compendium.

    Note: This function was designed to processed data from the pseudomonas
    compendium defined in the ADAGE paper
    (https://msystems.asm.org/content/1/1/e00025-15).
    """

    # Create processed pseudomonas compendium data file
    raw_compendium = pd.read_csv(raw_filename, header=0, index_col=0, sep="\t")

    if raw_compendium.shape[1] != 5549:
        processed_compendium = raw_compendium.T
    else:
        processed_compendium = raw_compendium

    assert processed_compendium.shape[1] == 5549

    # Save transformed compendium data
    processed_compendium.to_csv(processed_filename, sep="\t")

    # Normalize processed pseudomonas compendium data
    normalize_compendium(processed_filename, normalized_filename, scaler_filename)


def process_raw_compendium_recount2(
    raw_filename,
    gene_id_filename,
    manual_mapping,
    DE_prior_filename,
    shared_genes_filename,
    mapped_filename,
    normalized_filename,
    scaler_filename,
):
    """
    Create mapped recount2 compendium data file based on raw compendium
    data file (`raw_filename`), and normalize the mapped compendium.
    """

    # Create mapped recount2 compendium data file
    map_recount2_data(
        raw_filename,
        gene_id_filename,
        manual_mapping,
        DE_prior_filename,
        shared_genes_filename,
        mapped_filename,
    )

    # Normalize mapped recount2 compendium data
    normalize_compendium(mapped_filename, normalized_filename, scaler_filename)


# TO DO:
# Either move to a plot.py function or remove if not needed with new changes
# Functions related to visualizing trends in generic
# genes/pathways found
# * function to generate summary dataframes
# * function to plot trends
# * function to compare groups of genes


def merge_abs_raw_dfs(abs_df, raw_df, condition):
    """
    This function merges and returns dataframe containing
    summary gene results using absolute value of the test
    statistic and raw test statistic values.

    Arguments
    ---------
    abs_df: df
        Summary df using absolute value of test statistic
    raw_df: df
        Summary df using raw value of test statistic
    condition: str
        Condition from E-GEOD-33245. Either '1v2', '1v3', '1v4' or '1v5'
    """
    merged_df = abs_df.merge(
        raw_df,
        left_on="Gene ID",
        right_on="Gene ID",
        suffixes=[f"_grp_{condition}", f"_grp_{condition}_raw"],
    )

    return merged_df


def merge_two_conditions_df(
    merged_condition_1_df, merged_condition_2_df, condition_1, condition_2
):
    """
    This function merges and returns summary dataframes across two conditions to
    compare trends. For example, merge summary dataframes between 1v2 and 1v3.

    Arguments
    ---------
    merged_condition_1_df: df
        df of results for one of the E-GEOD-33245 conditions ('1v2', '1v3', '1v4' or '1v5')
        returned from `merge_abs_raw_dfs`
    merged_condition_2_df: df
        df of results for another one of the E-GEOD-33245 conditions ('1v2', '1v3', '1v4' or '1v5')
        returned from `merge_abs_raw_dfs`
    condition_1: str
        Condition from E-GEOD-33245 associated with 'merged_condition_1_df'.
        Either '1v2', '1v3', '1v4' or '1v5'
    condition_2: str
        Condition from E-GEOD-33245 associated with 'merged_condition_2_df'.
        Either '1v2', '1v3', '1v4' or '1v5'
    """
    merged_all_df = merged_condition_1_df.merge(
        merged_condition_2_df, left_on="Gene ID", right_on="Gene ID"
    )
    merged_all_df["max Z score"] = (
        merged_all_df[
            [f"abs(Z score)_grp_{condition_1}", f"abs(Z score)_grp_{condition_2}"]
        ]
        .abs()
        .max(axis=1)
    )
    merged_all_df["Gene ID Name"] = (
        merged_all_df["Gene ID"]
        + " "
        + merged_all_df[f"Gene Name_grp_{condition_1}"].fillna("")
    )

    merged_df = merged_all_df[
        [
            "Gene ID",
            "Gene ID Name",
            f"Test statistic (Real)_grp_{condition_1}",
            f"Test statistic (Real)_grp_{condition_1}_raw",
            f"Adj P-value (Real)_grp_{condition_1}",
            f"Mean test statistic (simulated)_grp_{condition_1}",
            f"Std deviation (simulated)_grp_{condition_1}",
            f"Median adj p-value (simulated)_grp_{condition_1}",
            f"Test statistic (Real)_grp_{condition_2}",
            f"Test statistic (Real)_grp_{condition_2}_raw",
            f"Adj P-value (Real)_grp_{condition_2}",
            f"Mean test statistic (simulated)_grp_{condition_2}",
            f"Std deviation (simulated)_grp_{condition_2}",
            f"Median adj p-value (simulated)_grp_{condition_2}",
            f"abs(Z score)_grp_{condition_1}",
            f"abs(Z score)_grp_{condition_2}",
            "max Z score",
        ]
    ]
    return merged_df

def fetch_template_experiment(
    normalized_compendium_filename,
    metadata_filename,
    metadata_delimiter,
    experiment_id_colname,
    selected_experiment_id,
    sample_id_colname,
    scaler_filename,
    raw_template_filename,
    normalized_template_filename
):
    """
    This function will save the normalized and un-normalized version
    of the template experiment to the input filenames
    """
    # Read data
    normalized_compendium = pd.read_csv(
        normalized_compendium_filename, header=0, sep="\t", index_col=0
    )
    
    # Get corresponding sample ids
    sample_ids = simulate_expression_data.get_sample_ids(
        metadata_filename,
        metadata_delimiter,
        experiment_id_colname,
        selected_experiment_id,
        sample_id_colname,
    )

    # Gene expression data for selected samples
    template_normalized = normalized_compendium.loc[sample_ids]
    
    # Load pickled file
    scaler = pickle.load(open(scaler_filename, "rb"))
    
    # Un-normalize the data using scaler transform in order to run DE analysis downstream
    template_unnormalized = scaler.inverse_transform(template_normalized)

    template_unnormalized_df = pd.DataFrame(
        template_unnormalized,
        columns=template_normalized.columns,
        index=template_normalized.index,
    )
    
    # Save normalized template
    template_normalized.to_csv(normalized_template_filename, sep="\t")
    
    # Save un-normalized template
    template_unnormalized_df.to_csv(raw_template_filename, sep="\t")