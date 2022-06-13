Here we use an existing trained VAE model and simulate a background dataset using a template experiment that is **not included** in the training dataset (i.e. the datasets used to train the VAE model).

## Usage
1. Create a configuration and metadata files for your analysis. 

See [example configuration file]().
When editing this configuration file, use a text editor instead of excel.

The definition for each paramter in the configuation file is describe below:

Parameters for input data files and directories to create

| Name | Description |
| :--- | :---------- |
| base_dir| str: Root directory containing analysis subdirectories. By default the path is one level up from where the scripts are run.|
| local_dir| str: Parent directory on local machine to store intermediate results. Make sure to end path name with "/"|
| dataset_name| str: Name for analysis directory, which contains the notebooks being run. For example, this analysis directory is named "pre_model_unseen_template".|
| raw_template_filename | str: Downloaded template gene expression data file. The input dataset should be a matrix that is sample x gene. The file should tab-delimited. The gene ids need to be consistent between the template and compendium datasets. The input dataset should be generated using the same platform as the model you plan to use (i.e. RNA-seq or array). The expression values are expected to have been uniformly processed and can be estimated counts (RNA-seq) or log2 expression (array).|
| normalized_compendium_filename | str: The location of the normalized compendium gene expression data file. Normalized data can be found here: [recount2 normalized](https://storage.googleapis.com/recount2/normalized_recount2_compendium.tsv), [Powers et al. normalized](https://storage.googleapis.com/powers_et_al/normalized_rani_compendium_filename.tsv), [P. aeruginosa normalized](https://storage.googleapis.com/pseudomonas/normalized_pseudomonas_compendium_data.tsv).|
| project_id | str:  The experiment id to use as template experiment. This experiment is **not contained** within the training dataset that was used to train the VAE. The id is used to name intermediate simulated data files created.|
| num_simulated| int: The number of experiments to simulate. Experiments are simulated by shifting the template experiment in the latent space. In general, [Lee et al., Figure S4](https://www.biorxiv.org/content/10.1101/2021.05.24.445440v3) found that downstream statistical results were robust to different numbers of simulated experiments so starting with 25 experiments can compromise on the runtime of the downstream analyses. |
| vae_model_dir | str:  The location where the VAE model files (.h5) are stored.|
| scaler_filename | str: The location where the scaler file is stored. This file was generated during the VAE training process.|
| DE_method| str: "limma" or "DESeq". Differential expression method to use.|

Parameters for intermediate files created. Names of files need to be specified:
*Note: These file paths need to be created for the user in order to be used.*

| Name | Description |
| :--- | :---------- |
| normalized_template_filename | str: Normalized template gene expression data filename. The template experiment is normalized using the same scaler transform that was used to 0-1 scale the normalized compendium used to train the VAE (scaler_filename).|


2. Create metadata files that specify how samples within the selected template experiment should be grouped for the differential expression analysis.
By default, a two-condition differential expression analysis is supported (case vs control). 
In the metadata file, "1"s denote controls and "2"s denote cases.  
An example can be seen [here]()

3. Run notebooks in order
