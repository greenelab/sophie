# SOPHIE
Software to distinguish between common and experiment-specific gene expression signals

**Alexandra J. Lee and Casey S. Greene 2022**

**University of Pennsylvania**

This repository is named after the the character [Sophie](https://en.wikipedia.org/wiki/Ponyo), from Hayao Miyazaki's animated film *Howl's moving castle*. 
In the film, Sophie’s appearance as an old woman, despite being a young woman that has been cursed, shows that initial observation can be misleading. 
Likewise SOPHIE allows users to identify specific gene expression signatures that can be masked by common background patterns. 

SOPHIE was originally described and applied in [generi-expression-patterns](https://github.com/greenelab/generic-expression-patterns) repository.

## Installation

TBD

## Usage
There are 4 ways SOPHIE can be applied:

| Type | Description |
| :--- | :---------- |
| Existing model and template experiment in training dataset| Here we use an existing trained VAE model and simulate a background dataset using a template experiment that is included in the training dataset that was used to train the VAE model. |
| Existing model and template experiment not in training dataset| Here we use an existing trained VAE model and simulate a background dataset using a template experiment that is *not* included in the training dataset that was used to train the VAE model.|
| New model and template experiment in training dataset| Here we train a new VAE model. Then simulate a background dataset using a template experiment that is included in the training dataset that was used to train the new VAE model. |
| New model and template experiment not in training dataset| Here we train a new VAE model. Then simulate a background dataset using a template experiment that is *not* included in the training dataset that was used to train the VAE model.|