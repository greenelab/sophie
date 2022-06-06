Here we use an existing trained VAE model and simulate a background dataset using a template experiment that is included in the training dataset (i.e. the datasets used to train the VAE model).


1. Create a configuration and metadata files for your analysis. 

See [example configuration file]().
When editing this configuration file, use a text editor instead of excel.

The definition for each paramter in the configuation file is describe below:

Parameters for input data files and directories to create

| Name | Description |
| :--- | :---------- |
| base_dir| str: Root directory containing analysis subdirectories. By default the path is one level up from where the scripts are run.|
| local_dir| str: Parent directory on local machine to store intermediate results. Make sure to end path name with "/"|
| dataset_name| str: Name for analysis directory, which contains the notebooks being run. For example, this analysis directory is named "pre_model_seen_template".|
| raw_template_filename | str: Downloaded template gene expression data file. The input dataset should be a matrix that is sample x gene. The file should tab-delimited. The gene ids should be HGNC symbols (if using human data) or PA numbers (if using *P. aeruginosa* data). The input dataset should be generated using the same platform as the model you plan to use (i.e. RNA-seq or array). The expression values are expected to have been uniformly processed and can be estimated counts (RNA-seq) or log2 expression (array).|
| raw_compendium_filename | str: Downloaded compendium gene expression data file. The input dataset should be a matrix that is sample x gene. The file should tab-delimited. The gene ids should be HGNC symbols (if using human data) or PA numbers (if using *P. aeruginosa* data). The input dataset should be generated using the same platform as the model you plan to use (i.e. RNA-seq or array). The expression values are expected to have been uniformly processed and can be estimated counts (RNA-seq) or log2 expression (array).|
| experiment_to_sample_filename | str:  File mapping experiment ids to sample ids|
| metadata_delimiter | str:  Delimiter ("," or "\t") used in the metadata file that maps experiment id to sample ids|
| experiment_id_colname | str:  Header of experiment-to-sample metadata file corresponding to the column containing experiment ids. This is used to extract gene expression data associated with project_id|
| sample_id_colname | str:   Header of experiment-to-sample metadata file to indicate column containing sample ids.This is used to extract gene expression data associated with project_id|
| project_id | str:  The experiment id to use as template experiment. This experiment must be contained within the training dataset that was used to train the VAE. The id is using the values found in the <metadata_experiment_colname> column of the <experiment_to_sample_filename>. This <project_id> corresponds to a group of samples that were used to test an single hypothesis. This parameter is needed if using either latent transformation approaches.|
| num_simulated| int: The number of experiments to simulate. Experiments are simulated by shifting the template experiment in the latent space.|
| scaler_filename | str: The location where the scaler file is stored. This file was generated during the VAE training process.|

Parameters for intermediate files created. Names of files need to be specified:

| Name | Description |
| :--- | :---------- |
| normalized_template_filename | str: Normalized template gene expression data file.|
| normalized_compendium_filename | str: Normalized compendium gene expression data file.|

2. Create metadata files that specify how samples within your selected template experiment should be grouped for the differential expression analysis. 
An example can be seen [here]()

3. Run notebooks in order
