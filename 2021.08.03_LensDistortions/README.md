# Lens Distortions

## Purpose

This code was used to create the figures found in the series "Lens Distortions",
which dealt with understanding lens distortions in camera models.

## Blog post

- 2021.08.06: [Camera Modeling: Exploring Distortion and Distortion Models, Part
  I](https://www.tangramvision.com/blog/camera-modeling-exploring-distortion-and-distortion-models-part-i)
- 2021.08.09: [Camera Modeling: Exploring Distortion and Distortion Models, Part
  II](https://www.tangramvision.com/blog/camera-modeling-exploring-distortion-and-distortion-models-part-ii)

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
In [1]: %run lens_distortions.py
```

