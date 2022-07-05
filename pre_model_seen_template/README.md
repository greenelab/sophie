Here we use an existing trained VAE model and simulate a background dataset using a template experiment that is included in the training dataset (i.e. the datasets used to train the VAE model).

## Usage
1. Create a configuration file for your analysis. See [example configuration file](config_example.tsv). The definition for each paramter in the configuation file is describe below.

Note: When editing this configuration file, use a text editor instead of excel.

Parameters for input data files and directories to create

| Name | Description |
| :--- | :---------- |
| base_dir| str: Root directory containing analysis subdirectories. By default the path is one level up from where the scripts are run.|
| local_dir| str: Parent directory on local machine to store intermediate results. Make sure to end path name with "/". This directory is created by https://github.com/greenelab/ponyo/blob/master/ponyo/utils.py|
| dataset_name| str: Name for analysis directory, which contains the notebooks being run. For example, this analysis directory is named "pre_model_seen_template".|
| normalized_compendium_filename | str: The location of the normalized compendium gene expression data file. Normalized data can be found here: [recount2 normalized](https://storage.googleapis.com/recount2/normalized_recount2_compendium.tsv), [Powers et al. normalized](https://storage.googleapis.com/powers_et_al/normalized_rani_compendium_filename.tsv), [P. aeruginosa normalized](https://storage.googleapis.com/pseudomonas/normalized_pseudomonas_compendium_data.tsv).|
| metadata_filename | str:  File mapping experiment ids to sample ids.|
| metadata_delimiter | str:  Delimiter ("," or "\t") used in the metadata file that maps experiment id to sample ids.|
| metadata_experiment_colname | str:  Header of metadata_filename corresponding to the column containing experiment ids. This is used to extract gene expression data associated with project_id.|
| metadata_sample_colname | str:   Header of metadata_filename to indicate column containing sample ids.This is used to extract gene expression data associated with project_id.|
| project_id | str:  The experiment id to use as template experiment. This experiment must be contained within the training dataset that was used to train the VAE. The id is using the values found in the <metadata_experiment_colname> column of the <experiment_to_sample_filename>. This <project_id> corresponds to a group of samples that were used to test an single hypothesis. This parameter is used to pull out the template expression data from the normalized compendium and to simulate data based on this experiment.|
| num_simulated| int: The number of experiments to simulate. Experiments are simulated by shifting the template experiment in the latent space. In general, [Lee et al., Figure S4](https://www.biorxiv.org/content/10.1101/2021.05.24.445440v3) found that downstream statistical results were robust to different numbers of simulated experiments so starting with 25 experiments can compromise on the runtime of the downstream analyses. |
| simulated_data_dir | str:  The location where the simulated experiments are written to. This directory is created by https://github.com/greenelab/ponyo/blob/master/ponyo/utils.py|
| vae_model_dir | str:  The location where the existing VAE model files (.h5) are stored.|
| latent_dim | int:  The latent dimension size. If using recount2 its 30, if using Powers et al. its 30, if using P. aeruginosa its 30.|
| scaler_transform_filename | str: The location where the scaler file is stored. This file was generated during the VAE training process. The scaler files can be found [here](data/scalers/)|
| DE_method| str: "limma" or "deseq". Differential expression method to use.|
| count_threshold | int: Remove genes that have mean count <= count_threshold. By default this threshold is set to None, then no genes are removed.|
| template_process_samples_filename | str: Metadata file that maps sample ids to labels that indicate if the sample is kept or discarded. By default, a two-condition differential expression analysis is supported (case vs control). However, some experiments included more than 2 conditions and so these "extra" samples should not considered in the downstream differential expression analysis. This file contains 2 columns that are tab-delimited. The first column contains sample ids and the second column contains the group id: "1"s denote controls, "2"s denote cases and "drop" denotes samples to remove. For example, say there is an experiment that contains WT samples, mutant A samples and mutant B samples. Since we assume a two-condition experiment, we will remove all mutant B samples so that we can compare WT vs mutant A samples.|
| template_DE_grouping_filename | str: Metadata file that maps sample ids to groups for differential expression analysis. By default, a two-condition differential expression analysis is supported (case vs control). This file contains 2 columns that are tab-delimited. The first column contains sample ids and the second column contains the group id: "1"s denote controls and "2"s denote cases. |
| rank_genes_by | str: "log2FoldChange" if using DESeq or "log2FC" if using limma. |

Parameters for intermediate files created. Names of files need to be specified:
*Note: Ensure the directory containing these files exists.*

| Name | Description |
| :--- | :---------- |
| raw_template_filename | str: Un-normalized template gene expression data filename. This file is generated by reverse transforming the data using the scaler_filename. The data in this raw_template filename will be used to compare gene expression changes in reference to a compendium of simulated experiments.|
| normalized_template_filename | str: Normalized template gene expression data filename.|
| processed_template_filename | str: Processed template gene expression data filename. This file contains gene expression data after extra samples have been dropped based on `template_process_samples_filename` and count thresholding applied.|
| output_filename | str: Filename containing the SOPHIE results.|


2. Create metadata files that specify how samples within the selected template experiment should be grouped for the differential expression analysis.
By default, a two-condition differential expression analysis is supported (case vs control). In the metadata file, "1"s denote controls and "2"s denote cases. In the metadata file, "1"s denote controls and "2"s denote cases. This file is specified by the `template_DE_grouping_filename` parameter. An example can be seen [here](SRP012656_groups.tsv)

3. Run notebooks in order
