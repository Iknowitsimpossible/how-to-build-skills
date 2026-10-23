# Template: Data analysis / ML

A visitor wants to know: what question was asked, what was found, and can I reproduce it?

## Skeleton

````markdown
# Project Title

One sentence: the question or task, and the headline result.

## What it does

- **Goal:** what was being predicted, analyzed, or explored
- **Data:** source, size, and link (and license if known)
- **Approach:** methods/models, in one or two lines
- **Results:** the key number or finding, with one figure

![Key result](figures/result.png)

## Installation

```bash
git clone https://github.com/user/repo.git
cd repo
pip install -r requirements.txt     # or: conda env create -f environment.yml
```

Getting the data: explain how, if it isn't in the repo.

## Usage

Run order:

1. `notebooks/01_cleaning.ipynb`: cleans the raw data
2. `notebooks/02_model.ipynb`: trains and evaluates

or

```bash
python train.py --config configs/base.yaml
```

## Project structure   <!-- short tree of data/, notebooks/, src/ -->
````

## Type-specific notes

- **Lead with the result.** Readers of data projects care about findings. Take numbers from notebook outputs or results files. Never round or embellish them.
- **Data access:** if the data is gitignored or too large, explain where to download it and where to put it. Note the license or terms of use if known.
- **Run order:** if notebooks are numbered or depend on each other, list them in order with one line each.
- **Reproducibility:** mention random seeds, GPU requirements, or long runtimes if the code shows them.
