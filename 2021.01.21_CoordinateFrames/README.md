# Coordinate Frames

## Purpose

This code was used to create the figures found in the series "Coordinate
Frames", which dealt with methods to transition between spatial frames of
reference.

## Blog post

- 2021.01.21: [Coordinate systems, and how to relate multiple coordinate frames together, Part
  I](https://www.tangramvision.com/blog/coordinate-systems-and-how-to-relate-multiple-coordinate-frames-together-part-1)

- 2021.04.08: [Coordinate systems, and how to relate multiple coordinate frames together, Part
  II](https://www.tangramvision.com/blog/rotate-scale-translate-coordinate-frames-for-multi-sensor-systems-part-2)

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
In [1]: %run CoordinateFrames.py
```

