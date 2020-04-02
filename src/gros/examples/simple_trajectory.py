#!/usr/bin/env python

from numpy import pi

from gros.metric import schwarzschild as ss
from gros.utils import const


def simple_trajectory():
    # Initialize metric

    # ss_metric = ss.SchwarzschildMetric(
    #     M=const.M_solar,
    #     initial_vec_pos=[46e6 * 1000, pi/2, 0],
    #     initial_vec_v=[0, 0, (47362 / 46e6)]
    # )

    # TODO: move initial vecs into calculate_trajectory method
    # TODO: put proper time, coordinate time to plot and animation
    # TODO: faster animation with frames!
    ss_metric = ss.SchwarzschildMetric(
        M=const.M_earth,
        initial_vec_pos=[140, pi/2, 0],
        initial_vec_v=[0, 0, 1800]
    )

    traj = ss_metric.calculate_trajectory(proptime_end=0.002, step_size=5e-7)
    traj.plot()


if __name__ == "__main__":
    simple_trajectory()
