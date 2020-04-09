#!/usr/bin/env python

from numpy import pi

from gros.metric import schwarzschild as ss
from gros.utils import const


def earth_black_hole_trajectory():
    ss_metric = ss.SchwarzschildMetric(
        M=const.M_earth,
        initial_vec_pos=[100, pi/2, 0],
        initial_vec_v=[0, 0, 5000]
    )

    traj = ss_metric.calculate_trajectory(proptime_end=0.005, step_size=1e-5)
    traj.plot()


if __name__ == "__main__":
    earth_black_hole_trajectory()
