use argmin::prelude::*;
use nalgebra as na;

fn skew_sym(v: na::Vector3<f64>) -> na::Matrix3<f64> {
    let mut ss = na::Matrix3::zeros();
    ss[(0, 1)] = -v[2];
    ss[(0, 2)] = v[1];
    ss[(1, 0)] = v[2];
    ss[(1, 2)] = -v[0];
    ss[(2, 0)] = -v[1];
    ss[(2, 1)] = v[0];
    ss
}

fn exp_map(param_vector: &na::Vector6<f64>) -> na::Isometry3<f64> {
    let t = param_vector.fixed_slice::<3, 1>(0, 0);
    let omega = param_vector.fixed_slice::<3, 1>(3, 0);
    let theta = omega.norm();
    let half_theta = 0.5 * theta;
    let quat_axis = omega * half_theta.sin() / theta;
    let quat = if theta > 1e-6 {
        na::UnitQuaternion::from_quaternion(na::Quaternion::new(
            half_theta.cos(),
            quat_axis.x,
            quat_axis.y,
            quat_axis.z,
        ))
    } else {
        na::UnitQuaternion::identity()
    };

    let mut v = na::Matrix3::<f64>::identity();
    if theta > 1e-6 {
        let ssym_omega = skew_sym(omega.clone_owned());
        v += ssym_omega * (1.0 - theta.cos()) / (theta.powi(2))
            + (ssym_omega * ssym_omega) * ((theta - theta.sin()) / (theta.powi(3)));
    }

    let trans = na::Translation::from(v * t);

    na::Isometry3::from_parts(trans, quat)
}

fn log_map(input: &na::Isometry3<f64>) -> na::Vector6<f64> {
    let t: na::Vector3<f64> = input.translation.vector;

    let quat = input.rotation;
    let theta: f64 = 2.0 * (quat.scalar()).acos();
    let half_theta = 0.5 * theta;
    let mut omega = na::Vector3::<f64>::zeros();

    let mut v_inv = na::Matrix3::<f64>::identity();
    if theta > 1e-6 {
        let ssym_omega = skew_sym(omega);
        v_inv -= ssym_omega * 0.5;
        v_inv += ssym_omega * ssym_omega * (1.0 - half_theta * half_theta.cos() / half_theta.sin())
            / (theta * theta);
        omega = quat.vector() * theta / (half_theta.sin());
    }

    let mut ret = na::Vector6::<f64>::zeros();
    ret.fixed_slice_mut::<3, 1>(0, 0).copy_from(&(v_inv * t));
    ret.fixed_slice_mut::<3, 1>(3, 0).copy_from(&omega);

    ret
}

fn exp_map_jacobian(transformed_point: &na::Point3<f64>) -> na::Matrix3x6<f64> {
    let mut ss = na::Matrix3x6::zeros();
    ss.fixed_slice_mut::<3, 3>(0, 0)
        .copy_from(&na::Matrix3::<f64>::identity());
    ss.fixed_slice_mut::<3, 3>(0, 3)
        .copy_from(&(-skew_sym(transformed_point.coords)));
    ss
}

fn project(
    params: &na::Vector4<f64>, /*fx, fy, cx, cy*/
    pt: &na::Point3<f64>,
) -> na::Point2<f64> {
    na::Point2::<f64>::new(
        params[0] * pt.x / pt.z + params[2], // fx * x / z + cx
        params[1] * pt.y / pt.z + params[3], // fy * y / z + cy
    )
}

fn proj_jacobian_wrt_params(transformed_pt: &na::Point3<f64>) -> na::Matrix2x4<f64> {
    na::Matrix2x4::<f64>::new(
        transformed_pt.x / transformed_pt.z,
        0.0,
        1.0,
        0.0,
        0.0,
        transformed_pt.y / transformed_pt.z,
        0.0,
        1.0,
    )
}

fn proj_jacobian_wrt_point(
    camera_model: &na::Vector4<f64>, /*fx, fy, cx, cy*/
    transformed_pt: &na::Point3<f64>,
) -> na::Matrix2x3<f64> {
    na::Matrix2x3::<f64>::new(
        camera_model[0] / transformed_pt.z,
        0.0,
        -transformed_pt.x * camera_model[0] / (transformed_pt.z.powi(2)),
        0.0,
        camera_model[1] / transformed_pt.z,
        -transformed_pt.y * camera_model[1] / (transformed_pt.z.powi(2)),
    )
}

struct Calibration<'a> {
    model_pts: &'a Vec<na::Point3<f64>>,
    image_pts_set: &'a Vec<Vec<na::Point2<f64>>>,
}

impl<'a> Calibration<'a> {
    /// Decode the camera model and transforms from the flattened parameter vector
    fn decode_params(
        &self,
        param: &na::DVector<f64>,
    ) -> (na::Vector4<f64>, Vec<na::Isometry3<f64>>) {
        // Camera parameters are in the first four elements
        let camera_model: na::Vector4<f64> = param.fixed_slice::<4, 1>(0, 0).clone_owned();

        // Following the camera parameters, for each image there
        // will be one 6D transform
        let transforms = self
            .image_pts_set
            .iter()
            .enumerate()
            .map(|(i, _)| {
                let lie_alg_transform: na::Vector6<f64> =
                    param.fixed_slice::<6, 1>(4 + 6 * i, 0).clone_owned();
                // Convert to a useable na::Isometry
                exp_map(&lie_alg_transform)
            })
            .collect::<Vec<_>>();
        (camera_model, transforms)
    }
}

impl ArgminOp for Calibration<'_> {
    /// Type of the parameter vector
    type Param = na::DVector<f64>;
    /// Type of the return value computed by the cost function
    type Output = na::DVector<f64>;
    /// Type of the Hessian. Can be `()` if not needed.
    type Hessian = ();
    /// Type of the Jacobian. Can be `()` if not needed.
    type Jacobian = na::DMatrix<f64>;
    /// Floating point precision
    type Float = f64;

    /// Calculate the residual vector
    fn apply(&self, p: &Self::Param) -> Result<Self::Output, Error> {
        let (camera_model, transforms) = self.decode_params(p);

        let num_images = self.image_pts_set.len();
        let num_target_points = self.model_pts.len();
        let num_residuals = num_images * num_target_points;

        let mut residual = na::DVector::<f64>::zeros(num_residuals * 2);

        let mut residual_idx = 0;
        for (image_pts, transform) in self.image_pts_set.iter().zip(transforms.iter()) {
            for (observed_image_pt, target_pt) in image_pts.iter().zip(self.model_pts.iter()) {
                // Apply image formation model
                let transformed_point = transform * target_pt;
                let projected_pt = project(&camera_model, &transformed_point);

                // Populate residual vector two rows at time
                let individual_residual = projected_pt - observed_image_pt;
                residual
                    .fixed_slice_mut::<2, 1>(residual_idx, 0)
                    .copy_from(&individual_residual);
                residual_idx += 2;
            }
        }

        Ok(residual)
    }

    /// Calculate the jacobian
    fn jacobian(&self, p: &Self::Param) -> Result<Self::Jacobian, Error> {
        let (camera_model, transforms) = self.decode_params(p);
        let num_images = self.image_pts_set.len();
        let num_target_points = self.model_pts.len();
        let num_residuals = num_images * num_target_points;
        let num_unknowns = 6 * num_images + 4;

        let mut jacobian = na::DMatrix::<f64>::zeros(num_residuals * 2, num_unknowns);

        let mut residual_idx = 0;
        for ((i, _), transform) in self.image_pts_set.iter().enumerate().zip(transforms.iter()) {
            for target_pt in self.model_pts.iter() {
                // Apply image formation model
                let transformed_point = transform * target_pt;

                // Populate jacobian matrix two rows at time
                jacobian
                    .fixed_slice_mut::<2, 4>(residual_idx, 0)
                    .copy_from(&proj_jacobian_wrt_params(&transformed_point)); // params jacobian

                let proj_jacobian_wrt_point =
                    proj_jacobian_wrt_point(&camera_model, &transformed_point);
                let transform_jacobian_wrt_transform = exp_map_jacobian(&transformed_point);
                jacobian
                    .fixed_slice_mut::<2, 6>(residual_idx, 4 + i * 6)
                    .copy_from(&(proj_jacobian_wrt_point * transform_jacobian_wrt_transform)); // transform jacobian

                residual_idx += 2;
            }
        }
        Ok(jacobian)
    }
}

fn main() {
    // 11x11 pattern in a 1m x 1m square in the XY plane
    let mut source_pts: Vec<na::Point3<f64>> = Vec::new();
    for i in -5..6 {
        for j in -5..6 {
            source_pts.push(na::Point3::<f64>::new(i as f64 * 0.1, j as f64 * 0.1, 0.0));
        }
    }

    let camera_model = na::Vector4::<f64>::new(540.0, 540.0, 320.0, 240.0); // fx, fy, cx, cy

    let transforms = vec![
        na::Isometry3::<f64>::new(
            na::Vector3::<f64>::new(-0.1, 0.1, 2.0),
            na::Vector3::<f64>::new(-0.2, 0.2, 0.2),
        ),
        na::Isometry3::<f64>::new(
            na::Vector3::<f64>::new(-0.1, -0.1, 2.0),
            na::Vector3::<f64>::new(0.2, -0.2, 0.2),
        ),
        na::Isometry3::<f64>::new(
            na::Vector3::<f64>::new(0.1, 0.1, 2.0),
            na::Vector3::<f64>::new(-0.2, -0.2, -0.2),
        ),
    ];

    let transformed_pts = transforms
        .iter()
        .map(|t| source_pts.iter().map(|p| t * p).collect::<Vec<_>>())
        .collect::<Vec<_>>();

    let imaged_pts = transformed_pts
        .iter()
        .map(|t_list| {
            t_list
                .iter()
                .map(|t| project(&camera_model, t))
                .collect::<Vec<na::Point2<f64>>>()
        })
        .collect::<Vec<_>>();

    let cal_cost = Calibration {
        model_pts: &source_pts,
        image_pts_set: &imaged_pts,
    };

    let mut init_param = na::DVector::<f64>::zeros(4 + imaged_pts.len() * 6);

    // Arbitrary guess for camera model
    init_param[0] = 1000.0; // fx
    init_param[1] = 1000.0; // fy
    init_param[2] = 500.0; // cx
    init_param[3] = 500.0; // cy

    // Arbitrary guess for poses (3m in front of the camera with no rotation)
    // We have to convert this to a 6D lie algebra element to populate the parameter
    // vector
    let init_pose = log_map(&na::Isometry3::translation(0.0, 0.0, 3.0));

    // Populate poses with guess
    init_param
        .fixed_slice_mut::<6, 1>(4, 0)
        .copy_from(&init_pose);
    init_param
        .fixed_slice_mut::<6, 1>(4 + 6, 0)
        .copy_from(&init_pose);
    init_param
        .fixed_slice_mut::<6, 1>(4 + 6 * 2, 0)
        .copy_from(&init_pose);

    eprintln!("init: {:.02}", init_param);

    // Solve
    let solver = argmin::solver::gaussnewton::GaussNewton::new()
        .with_gamma(1e-1)
        .unwrap();
    let res = Executor::new(cal_cost, solver, init_param)
        .add_observer(ArgminSlogLogger::term(), ObserverMode::Always)
        .max_iters(2000)
        .run()
        .unwrap();

    eprintln!("{}\n\n", res);

    // Print intrinsics results
    eprintln!("ground truth intrinsics: {}", camera_model);
    eprintln!(
        "optimized intrinsics: {}",
        res.state().best_param.fixed_slice::<4, 1>(0, 0)
    );

    // Print transforms
    for (i, t) in transforms.iter().enumerate() {
        eprintln!("ground truth transform[{}]: {}", i, t);
        eprintln!(
            "optimized result[{}]: {}\n",
            i,
            exp_map(
                &res.state()
                    .best_param
                    .fixed_slice::<6, 1>(4 + 6 * i, 0)
                    .clone_owned()
            )
        );
    }
}
