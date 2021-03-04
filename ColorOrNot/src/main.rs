//! Simulates a grayscale, bayer, and nearest-neighbor image capture from a given image.
//!
//! This code uses bare-bones logic in a purposeful attempt to expose the math behind these simple algorithms. There are
//! better demosaicing algorithms out there, like linear/bilinear interpolation, but this program is only meant to
//! demonstrate the basics.
//!
//! Logic flow:
//!
//! - Imports the provided JPG image
//! - Converts it to grayscale, to simulate a monochrome capture (img_gray.jpg)
//! - Simulates a Bayer image capture on a BGGR pattern (img_bayer.jpg)
//! - Uses the simulated Bayer pattern to perform nearest-neighbor color interpolation (img_nn.jpg)
//!
//! All images are saved to /tmp.

use anyhow::Result;
use image::{open, Rgb};

/// Create our bayer image.
///
/// Pattern for us is BGGR; to show this, zero out the other
/// components that wouldn't be represented in the image.
fn create_bayer_img(
    img_rgb_flat: image::FlatSamples<std::vec::Vec<u8>>,
    width: u32,
    height: u32,
) -> image::FlatSamples<std::vec::Vec<u8>> {
    let mut img_bayer_flat = img_rgb_flat;
    for x in 0..width {
        for y in 0..height {
            // top left is B
            if x % 2 == 0 && y % 2 == 0 {
                *img_bayer_flat.get_mut_sample(0, x, y).unwrap() = 0;
                *img_bayer_flat.get_mut_sample(1, x, y).unwrap() = 0;
            }
            // top right is G, bottom left is G
            else if (x % 2 == 1 && y % 2 == 0) || (x % 2 == 0 && y % 2 == 1) {
                *img_bayer_flat.get_mut_sample(0, x, y).unwrap() = 0;
                *img_bayer_flat.get_mut_sample(2, x, y).unwrap() = 0;
            }
            // bottom right is R
            else if x % 2 == 1 && y % 2 == 1 {
                *img_bayer_flat.get_mut_sample(1, x, y).unwrap() = 0;
                *img_bayer_flat.get_mut_sample(2, x, y).unwrap() = 0;
            }
        }
    }
    img_bayer_flat
}

fn nearest_neighbor_demosaicing(
    img_bayer_flat: image::FlatSamples<std::vec::Vec<u8>>,
    width: u32,
    height: u32,
) -> image::FlatSamples<std::vec::Vec<u8>> {
    // Create nearest-neighbor interpolated image from our BGGR bayer pattern
    let mut img_nn_flat = img_bayer_flat;
    for x in 0..width {
        for y in 0..height {
            // top left is B
            if x % 2 == 0 && y % 2 == 0 {
                // r from the bottom right
                *img_nn_flat.get_mut_sample(0, x, y).unwrap() =
                    *img_nn_flat.get_mut_sample(0, x + 1, y + 1).unwrap();
                // g from the top right
                *img_nn_flat.get_mut_sample(1, x, y).unwrap() =
                    *img_nn_flat.get_mut_sample(1, x + 1, y).unwrap();
            }
            // top right is G
            else if x % 2 == 1 && y % 2 == 0 {
                // r from the bottom right
                *img_nn_flat.get_mut_sample(0, x, y).unwrap() =
                    *img_nn_flat.get_mut_sample(0, x, y + 1).unwrap();
                // b from the top left
                *img_nn_flat.get_mut_sample(2, x, y).unwrap() =
                    *img_nn_flat.get_mut_sample(2, x - 1, y).unwrap();
            }
            // bottom left is G
            else if x % 2 == 0 && y % 2 == 1 {
                // r from the bottom right
                *img_nn_flat.get_mut_sample(0, x, y).unwrap() =
                    *img_nn_flat.get_mut_sample(0, x + 1, y).unwrap();
                // b from the top left
                *img_nn_flat.get_mut_sample(2, x, y).unwrap() =
                    *img_nn_flat.get_mut_sample(2, x, y - 1).unwrap();
            }
            // bottom right is R
            if x % 2 == 1 && y % 2 == 1 {
                // g from the bottom left
                *img_nn_flat.get_mut_sample(1, x, y).unwrap() =
                    *img_nn_flat.get_mut_sample(1, x - 1, y).unwrap();
                // b from the top left
                *img_nn_flat.get_mut_sample(2, x, y).unwrap() =
                    *img_nn_flat.get_mut_sample(2, x - 1, y - 1).unwrap();
            }
        }
    }
    img_nn_flat
}

fn main() -> Result<()> {
    // Import our image
    let mut current_dir = std::env::current_dir()?;
    current_dir.push("src/plexus36.jpg");
    let img = open(current_dir).unwrap();

    // Create and save our grayscale image
    let img_gray = img.clone().into_luma8();
    let mut dir = std::env::temp_dir();
    dir.push("img_gray.jpg");
    img_gray.save(dir)?;

    // Use our photo data as an 8-bit RGB image
    let img_rgb = img.into_rgb8();
    let width = img_rgb.width();
    let height = img_rgb.height();
    let img_rgb_flat = img_rgb.into_flat_samples();

    // Create and save our simulated bayer image from the imported photo
    let img_bayer_flat = create_bayer_img(img_rgb_flat, width, height);
    let mut dir = std::env::temp_dir();
    dir.push("img_bayer.jpg");
    if let Ok(img_bayer) = img_bayer_flat.clone().try_into_buffer::<Rgb<u8>>() {
        img_bayer.save(dir)?;
    }

    // Create and save our nearest-neighbor demosaiced image
    let img_nn_flat = nearest_neighbor_demosaicing(img_bayer_flat, width, height);
    let mut dir = std::env::temp_dir();
    dir.push("img_nn.jpg");
    if let Ok(img_nn) = img_nn_flat.try_into_buffer::<Rgb<u8>>() {
        img_nn.save(dir)?;
    }

    Ok(())
}
