# Introduction for EEG recording with g.tec Unicorn Hybrid

## Information

Repository showing the basics to register, plot and create the first experimental procedure and database with the Unicorn Hybrid Black EEG recorder in python3. The proposed repository is composed of several scripts:

- [pylsl_intro](pylsl_intro.py) giving an introduction to handle, inspect and save EEG signals from generic oscillator, biomedical or entertainment EEG recorder (available on [OpenVIBE](http://openvibe.inria.fr/supported-hardware/)).
- [pylsl_plot](pylsl_plot.py) giving a real time plot of the EEG signal.
- [play_vid](play_vid.py) and [play_intro](play_intro.py) respectively playing a video or an introduction screen for the experimentation.
- [intro_interface](intro_interface.py) proposing a pipeline to create a database as proposed by Katsigiannis and Ramzan in [DREAMER](https://ieeexplore-ieee-org.ressources-electroniques.univ-lille.fr/document/7887697). This last consisting to an EEG signals recorded during watching of video promoting specific emotion. [registration_pipeline](registration_pipeline.py) propose the whole pipeline for the dataset registration.

To simulate and manage the data pipe, the python code works with [OpenVibe](http://openvibe.inria.fr/) platform. The server allows the information transfer from recorder to python script.

## Installation and Dependencies

### General 

[OpenVibe v3.2.0](http://openvibe.inria.fr/downloads/)

### Python

[Playsound](https://github.com/TaylorSMarks/playsound)

OpenCV

Scikit-learn

[pylsl](https://github.com/chkothe/pylsl) 1.13.1

Full package installation with pip: `pip install -r requirement.txt` or anaconda `conda env create -f conda_environment.yml`


## Remarks

If you are interested in our work, don't hesitate to contact us (victor.delvigne[at]umons.ac.be). 

Wish you the best in your research projects! :bowtie:
