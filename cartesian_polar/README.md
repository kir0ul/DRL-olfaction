# Cartesian/polar environment version of the task

## Local setup 🚧

### Install

To setup the environment, run the following:
``` sh
git clone git@github.com:NiloufarRazmi/RL_Olfaction.git
cd RL_Olfaction/cartesian_polar
python -m venv .venv
source .venv/bin/activate
pip install -Ue .
```

### Run

Modify the `params.ini` config file, then run the following:
``` sh
runexp params.ini
```


## Setup on Oscar ☁️

### Install

To setup the environment, run the following:
``` sh
git clone git@github.com:NiloufarRazmi/RL_Olfaction.git
cd RL_Olfaction/cartesian_polar
module load python/3.11.0s-ixrhc3q
python -m venv .venv
. .venv/bin/activate
```
Modify the line where the virtualenv is activated in `slurm_job.sh` with the path of your own virtualenv.  # TODO: This should be a variable.

### Run

Modify the `params.ini` config file, then run the following:
``` sh
make slurm
```
