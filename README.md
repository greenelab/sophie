# SOPHIE: Specific cOntext Pattern Highlighting In Expression data
Software to distinguish between common and experiment-specific gene expression signals

**Alexandra J. Lee and Casey S. Greene 2022**

**University of Pennsylvania**

This repository is named after the the character [Sophie](https://en.wikipedia.org/wiki/Ponyo), from Hayao Miyazaki's animated film *Howl's moving castle*. 
In the film, Sophie’s appearance as an old woman, despite being a young woman that has been cursed, shows that initial observation can be misleading. 
Likewise SOPHIE allows users to identify specific gene expression signatures that can be masked by common background patterns. 

SOPHIE was originally described and applied in the [generic-expression-patterns](https://github.com/greenelab/generic-expression-patterns) repository.

## Usage
First you need to set up your local repository:
1. Download and install [github's large file tracker](https://git-lfs.github.com/).
2. Install [miniconda](https://docs.conda.io/en/latest/miniconda.html)
3. Clone the `sophie` repository by running the following command in the terminal:
```
git clone https://github.com/greenelab/sophie.git
```
Note: Git automatically detects the LFS-tracked files and clones them via http.

4. Navigate into cloned repo by running the following command in the terminal:
```
cd sophie
```
5. Set up conda environment by running the following command in the terminal:
```bash
bash install.sh
```
6. Navigate to any of the directories below to apply SOPHIE:

Name | Description |
| :--- | :---------- |
[pre_model_seen_template](pre_model_seen_template/) | Here we use an existing trained VAE model and simulate a background dataset using a template experiment that is included in the training dataset (i.e. the datasets used to train the VAE model). |
[pre_model_unseen_template](pre_model_unseen_template/) | Here we use an existing trained VAE model and simulate a background dataset using a template experiment that is **not included** in the training dataset (i.e. the datasets used to train the VAE model).|
[new_model_seen_template](new_model_seen_template/) | Here we train a new VAE model. Then simulate a background dataset using a template experiment that is included in the training dataset (i.e. the datasets used to train the VAE model). |
[new_model_unseen_template](new_model_unseen_template/) | Here we train a new VAE model. Then simulate a background dataset using a template experiment that is **not included** in the training dataset (i.e. the datasets used to train the VAE model).|