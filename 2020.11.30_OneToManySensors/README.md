# One to Many Sensors

## Purpose

This code was used to create the figures found in the series "One to Many
Sensors", which dealt with Kalman filters.

## Blog post

- 2020.11.30: [One To Many Sensors, Part
  I](https://www.tangramvision.com/blog/one-to-many-sensor-trouble-part-1)
- 2020.12.04: [One To Many Sensors, Part
  II](https://www.tangramvision.com/blog/one-to-many-sensor-trouble-part-2)

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
In [1]: %run oneToManySensors.py
```

