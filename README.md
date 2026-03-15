This repository is used for exploration of learner models for e-learning contexts by implementing different models
and simulating a learner based on these models. The results will be displayed in a dashboard for live interaction
and feedback.

# Installation

Tested with Python 3.12

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Usage

## Solara Dashboard

The dashboard uses [Solara](https://solara.dev/) and can be opened locally as such (with active venv):

```bash
solara run src/dashboard.py
```
