# Projective Compensation

## Purpose

This code was used to create the figures found in the post "Projective Compensation", which deals
with describing how changes in one parameter can affect errors in another parameter in an
optimization.

## Blog post

- 2022.04.05: [Projective Compensation in Calibration](https://www.tangramvision.com/blog/projective-compensation-in-calibration)

## Installation

```
python3 -m venv ~/.venv/tangram
source ~/.venv/tangram/bin/activate
pip install -r requirements.txt
```

## Usage

To run the code in isolation, we use iPython:

```
ipython --matplotlib=qt
In [1]: %run projective_compensation.py
```

