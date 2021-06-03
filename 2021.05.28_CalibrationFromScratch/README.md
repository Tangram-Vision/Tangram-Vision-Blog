# Calibration from Scratch

## Purpose

This crate provides an example camera calibration program.

Instead of working with real pictures of checkerboards and
extracting features from them, the example synthetically generates
features from ground truth camera parameters, model coordinates and
camera poses.

Most of the code involves the set up of a camera calibration
optimization problem. The parameters we're estimating are supplied
with reasonable guesses and then the optimization is ran to convergence.
The optimized results are printed along side their ground truth values
for comparison.

## Blog post

- 2021.05.28: [Camera Calibration From Scratch](https://www.tangramvision.com/blog/calibration-from-scratch-using-rust-part-1-of-3)

## Installation

This repository is written in Rust. Make sure you have Rust installed
and up-to-date before running.

## Usage

```cargo run --release```

