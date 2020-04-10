#!/usr/bin/env python

from numpy import pi

from gros.metric import schwarzschild as ss
from gros.utils import const


def earth_black_hole_trajectory():
    ss_metric = ss.SchwarzschildMetric(
        M=const.M_earth,
        initial_vec_pos=[30, pi/2, 0],
        initial_vec_v=[0, 0, 20000]
    )

    traj = ss_metric.calculate_trajectory(proptime_end=1.2e-4, step_size=1e-6)
    traj.plot(animation_step_size=1e-6)


if __name__ == "__main__":
    earth_black_hole_trajectory()
