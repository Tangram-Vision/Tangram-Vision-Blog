# Color (Or Not)

## Purpose

Simulates a grayscale, bayer, and nearest-neighbor image capture from a given
image.

This code uses bare-bones logic in a purposeful attempt to expose the math
behind these simple algorithms. There are better demosaicing algorithms out
there, like linear/bilinear interpolation, but this program is only meant to
demonstrate the basics.

Logic flow:

- Imports the provided JPG image
- Converts it to grayscale, to simulate a monochrome capture (img_gray.jpg)
- Simulates a Bayer image capture on a BGGR pattern (img_bayer.jpg)
- Uses the simulated Bayer pattern to perform nearest-neighbor color
  interpolation (img_nn.jpg)

All images are saved to /tmp.

## Blog post

- 2021.04.12: [Color \(Or Not\)](https://www.tangramvision.com/blog/)

## Installation

This repository is written in Rust. Make sure you have Rust installed before
running. All required assets are included in this directory.

## Usage

```cargo run```

