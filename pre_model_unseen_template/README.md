Here we use an existing trained VAE model and simulate a background dataset using a template experiment that is **not included** in the training dataset (i.e. the datasets used to train the VAE model).

## Usage
1. Create a configuration and metadata files for your analysis. See [example configuration file](config_example.tsv). The definition for each paramter in the configuation file is describe below.

Note: When editing this configuration file, use a text editor instead of excel.

Parameters for input data files and directories to create

| Name | Description |
| :--- | :---------- |
| base_dir| str: Root directory containing analysis subdirectories. By default the path is one level up from where the scripts are run.|
| local_dir| str: Parent directory on local machine to store intermediate results. Make sure to end path name with "/". This directory is created by https://github.com/greenelab/ponyo/blob/master/ponyo/utils.py|
| raw_compendium_filename| str: The location of the raw compendium expression data. Raw data can be found here: [recount2 raw](https://storage.googleapis.com/recount2/mapped_recount2_compendium.tsv), [P. aeruginosa raw](https://storage.googleapis.com/pseudomonas/processed_pseudomonas_compendium_data.tsv), [Powers et al. raw](https://storage.googleapis.com/powers_et_al/mapped_rani_compendium.tsv)|
| normalized_compendium_filename | str: The location of the normalized compendium gene expression data file. Normalized data can be found here: [recount2 normalized](https://storage.googleapis.com/recount2/normalized_recount2_compendium.tsv), [Powers et al. normalized](https://storage.googleapis.com/powers_et_al/normalized_rani_compendium_filename.tsv), [P. aeruginosa normalized](https://storage.googleapis.com/pseudomonas/normalized_pseudomonas_compendium_data.tsv).|
| project_id | str:  The experiment id to use as template experiment. This experiment is **not contained** within the training dataset that was used to train the VAE. The id is used to name intermediate simulated data files created.|
| raw_template_filename | str: Downloaded template gene expression data file. The input dataset should be a matrix that is sample x gene. The file should tab-delimited. The gene ids need to be consistent between the template and compendium datasets. The input dataset should be generated using the same platform as the model you plan to use (i.e. RNA-seq or array). The expression values are expected to have been uniformly processed and can be estimated counts (RNA-seq) or log2 expression (array).|
| num_simulated| int: The number of experiments to simulate. Experiments are simulated by shifting the template experiment in the latent space. In general, [Lee et al., Figure S4](https://www.biorxiv.org/content/10.1101/2021.05.24.445440v3) found that downstream statistical results were robust to different numbers of simulated experiments so starting with 25 experiments can compromise on the runtime of the downstream analyses. |
| simulated_data_dir | str:  The location where the simulated experiments are written to. This directory is created by https://github.com/greenelab/ponyo/blob/master/ponyo/utils.py|
| vae_model_dir | str:  The location where the existing VAE model files (.h5) are stored. Pre-trained model files can be found in [here](data/models/)|
| latent_dim | int:  The latent dimension size. If using recount2 its 30, if using Powers et al. its 30, if using P. aeruginosa its 30.|
| scaler_transform_filename | str: The location where the scaler file is stored. This file was generated during the VAE training process. The scaler files can be found [here](data/scalers/)|
| DE_method| str: "limma" or "deseq". Differential expression method to use.|
| count_threshold | int: Remove genes that have mean count <= count_threshold. By default this threshold is set to None, then no genes are removed.|
| template_process_samples_filename | str: Metadata file that maps sample ids to labels that indicate if the sample is kept or discarded. By default, a two-condition differential expression analysis is supported (case vs control). However, some experiments included more than 2 conditions and so these "extra" samples should not considered in the downstream differential expression analysis. This file contains 2 columns that are tab-delimited. The first column contains sample ids and the second column contains the group id: "1"s denote controls, "2"s denote cases and "drop" denotes samples to remove. For example, say there is an experiment that contains WT samples, mutant A samples and mutant B samples. Since we assume a two-condition experiment, we will remove all mutant B samples so that we can compare WT vs mutant A samples.|
| template_DE_grouping_filename | str: Metadata file that maps sample ids to groups for differential expression analysis. By default, a two-condition differential expression analysis is supported (case vs control). This file contains 2 columns that are tab-delimited. The first column contains sample ids and the second column contains the group id: "1"s denote controls and "2"s denote cases. |
| rank_genes_by | str: "log2FoldChange" if using DESeq or "log2FC" if using limma. |
| is_recount2| bool: True is the compendium dataset being used is recount2. This will determine how experiment ids are parsed for latent transformation approaches.|

Parameters for intermediate files created. Names of files need to be specified:
*Note: Ensure the directory containing these files exists.*

| Name | Description |
| :--- | :---------- |
| mapped_template_filename | str: Template gene expression data filename. This file is generated by scale transforming the data using the scaler_filename. The gene ids of the template file and the compendium file are matched.|
| normalized_template_filename | str: Normalized template gene expression data filename. The template experiment is normalized using the same scaler transform that was used to 0-1 scale the normalized compendium used to train the VAE (scaler_transform_filename).|
| processed_template_filename | str: Processed template gene expression data filename. This file contains gene expression data after extra samples have been dropped based on `template_process_samples_filename` and count thresholding applied.|
| output_filename | str: Filename containing the SOPHIE results.|


2. Create metadata files that specify how samples within the selected template experiment should be grouped for the differential expression analysis.
By default, a two-condition differential expression analysis is supported (case vs control). In the metadata file, "1"s denote controls and "2"s denote cases. This file is specified by the `template_DE_grouping_filename` parameter. An example can be seen [here](costello_groups.tsv).

3. Run notebooks in order
