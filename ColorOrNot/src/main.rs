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

/// Identify what color filter should be simulated for a given pixel.
///
/// This program simulates working with a BGGR Bayer filter. This means that every 2x2 pixel patch has follows this
/// pattern:
///
/// | B  | G1 |
/// | G2 | R  |
///
/// ...where B is blue, G1 and G2 are green, and R is red.
pub enum BayerColor {
    Red,
    GreenOne,
    GreenTwo,
    Blue,
}

/// Derive the simulated color filter value for a given pixel coordinate for a BGGR Bayer filter.
///
/// We can use some row+column logic to derive when a given pixel coordinate should have a B, G, or R filter at any
/// point in an image. We'll use this to create a synthetic Bayer image from a given RGB picture.
fn color_from_pixel_coord(x: u32, y: u32) -> BayerColor {
    if x % 2 == 0 && y % 2 == 0 {
        BayerColor::Blue
    } else if x % 2 == 1 && y % 2 == 0 {
        BayerColor::GreenOne
    } else if x % 2 == 0 && y % 2 == 1 {
        BayerColor::GreenTwo
    } else {
        BayerColor::Red
    }
}

fn create_bayer_img(
    img_rgb_flat: image::FlatSamples<std::vec::Vec<u8>>,
    width: u32,
    height: u32,
) -> image::FlatSamples<std::vec::Vec<u8>> {
    let mut img_bayer_flat = img_rgb_flat;
    for x in 0..width {
        for y in 0..height {
            match color_from_pixel_coord(x, y) {
                BayerColor::Blue => {
                    // Cancel out the red and green channels
                    *img_bayer_flat.get_mut_sample(0, x, y).unwrap() = 0;
                    *img_bayer_flat.get_mut_sample(1, x, y).unwrap() = 0;
                }
                BayerColor::GreenOne | BayerColor::GreenTwo => {
                    // Cancel out the red and blue channels
                    *img_bayer_flat.get_mut_sample(0, x, y).unwrap() = 0;
                    *img_bayer_flat.get_mut_sample(2, x, y).unwrap() = 0;
                }
                BayerColor::Red => {
                    // Cancel out the green and blue channels
                    *img_bayer_flat.get_mut_sample(1, x, y).unwrap() = 0;
                    *img_bayer_flat.get_mut_sample(2, x, y).unwrap() = 0;
                }
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
    let mut img_nn_flat = img_bayer_flat;
    for x in 0..width {
        for y in 0..height {
            match color_from_pixel_coord(x, y) {
                BayerColor::Blue => {
                    // Assign R from the bottom right
                    *img_nn_flat.get_mut_sample(0, x, y).unwrap() =
                        *img_nn_flat.get_mut_sample(0, x + 1, y + 1).unwrap();
                    // G from the top right
                    *img_nn_flat.get_mut_sample(1, x, y).unwrap() =
                        *img_nn_flat.get_mut_sample(1, x + 1, y).unwrap();
                }
                BayerColor::GreenOne => {
                    // R from the bottom right
                    *img_nn_flat.get_mut_sample(0, x, y).unwrap() =
                        *img_nn_flat.get_mut_sample(0, x, y + 1).unwrap();
                    // B from the top left
                    *img_nn_flat.get_mut_sample(2, x, y).unwrap() =
                        *img_nn_flat.get_mut_sample(2, x - 1, y).unwrap();
                }
                BayerColor::GreenTwo => {
                    // R from the bottom right
                    *img_nn_flat.get_mut_sample(0, x, y).unwrap() =
                        *img_nn_flat.get_mut_sample(0, x + 1, y).unwrap();
                    // B from the top left
                    *img_nn_flat.get_mut_sample(2, x, y).unwrap() =
                        *img_nn_flat.get_mut_sample(2, x, y - 1).unwrap();
                }
                BayerColor::Red => {
                    // G from the bottom left
                    *img_nn_flat.get_mut_sample(1, x, y).unwrap() =
                        *img_nn_flat.get_mut_sample(1, x - 1, y).unwrap();
                    // B from the top left
                    *img_nn_flat.get_mut_sample(2, x, y).unwrap() =
                        *img_nn_flat.get_mut_sample(2, x - 1, y - 1).unwrap();
                }
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
