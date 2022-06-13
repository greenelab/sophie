Here we train a new VAE model. Then simulate a background dataset using a template experiment that is included in the training dataset (i.e. the datasets used to train the VAE model).

## Usage
1. Create a configuration and metadata files for your analysis. 

See [example configuration file]().
When editing this configuration file, use a text editor instead of excel.

The definition for each paramter in the configuation file is describe below:

Parameters for input data files supplied by the user, directories that sophie will create, and parameters that control the execution behavior of sophie.

| Name | Description |
| :--- | :---------- |
| base_dir| str: Root directory containing analysis subdirectories. By default the path is one level up from where the scripts are run.|
| local_dir| str: Parent directory on local machine to store intermediate results. Make sure to end path name with "/"|
| dataset_name| str: Name for analysis directory, which contains the notebooks being run. For example, this analysis directory is named "new_model_seen_template".|
| raw_compendium_filename | str: Downloaded compendium gene expression data file. The input dataset should be a matrix that is sample x gene. The file should tab-delimited. The input dataset should be generated using the same platform as the model you plan to use (i.e. RNA-seq or array). The expression values are expected to have been uniformly processed and can be estimated counts (RNA-seq) or log2 expression (array).|
| experiment_to_sample_filename | str:  File mapping experiment ids to sample ids|
| metadata_delimiter | str:  Delimiter ("," or "\t") used in the metadata file that maps experiment id to sample ids|
| experiment_id_colname | str:  Header of experiment-to-sample metadata file corresponding to the column containing experiment ids. This is used to extract gene expression data associated with project_id|
| sample_id_colname | str:   Header of experiment-to-sample metadata file to indicate column containing sample ids.This is used to extract gene expression data associated with project_id|
| project_id | str:  The experiment id to use as template experiment. This experiment must be contained within the training dataset that was used to train the VAE. The id is using the values found in the <metadata_experiment_colname> column of the <experiment_to_sample_filename>. This <project_id> corresponds to a group of samples that were used to test an single hypothesis. This parameter is used to pull out the template expression data from the normalized compendium and to simulate data based on this experiment.|
| num_simulated| int: The number of experiments to simulate. Experiments are simulated by shifting the template experiment in the latent space. In general, [Lee et al., Figure S4](https://www.biorxiv.org/content/10.1101/2021.05.24.445440v3) found that downstream statistical results were robust to different numbers of simulated experiments so starting with 25 experiments can compromise on the runtime of the downstream analyses. |
| vae_model_dir | str:  The location where the VAE model files (.h5) are stored.|
| DE_method| str: "limma" or "DESeq". Differential expression method to use.|
| NN_architecture | str: Name of neural network architecture to use. Format 'NN_<intermediate layer>_<latent layer>'|
| learning_rate| float: Step size used for gradient descent. In other words, it's how quickly the  methods is learning|
| batch_size | str: Training is performed in batches. So this determines the number of samples to consider at a given time|
| epochs | int: Number of times to train over the entire input dataset|
| kappa | float: How fast to linearly ramp up KL loss|
| intermediate_dim| int: Size of the hidden layer|
| latent_dim | int: Size of the bottleneck layer|
| epsilon_std | float: Standard deviation of Normal distribution to sample latent space|
| validation_frac | float: Fraction of samples to use for validation in VAE training|

Parameters for intermediate files created. Names of files need to be specified:
*Note: These file paths need to be created for the user in order to be used.*

| Name | Description |
| :--- | :---------- |
| scaler_filename | str: The location where the scaler file is stored. This file was generated during the VAE training process.|
| normalized_compendium_filename | str: Normalized compendium gene expression data filename.| 
| raw_template_filename | str: Un-normalized template gene expression data filename. This file is generated using the project_id to select out the associated expression data. The data in this raw_template filename will be used to compare gene expression changes in reference to a compendium of simulated experiments.|

2. Create metadata files that specify how samples within the selected template experiment should be grouped for the differential expression analysis.
By default, a two-condition differential expression analysis is supported (case vs control). 
In the metadata file, "1"s denote controls and "2"s denote cases. 
An example can be seen [here]()

3. Run notebooks in order
