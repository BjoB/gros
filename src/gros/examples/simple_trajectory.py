#!/usr/bin/env python

from numpy import pi

from gros.metric import schwarzschild as ss
from gros.utils import const


def simple_trajectory():
    # Initialize metric

    ss_metric = ss.SchwarzschildMetric(
        M=const.M_solar,
        initial_vec_pos=[57.9e6 * 1000, pi/2, 0],
        initial_vec_v=[0, 0, (47.4 / 57.9e6)]
    )

    # TODO:
    # move initial vecs into calculate_trajectory method
    # add optional object radius for plot (add to metric initialization via "grav. center object")
    # put proper time, coordinate time to plot and animation
    # document plotting methods
    # faster animation with frames!
    # add planet / black hole data to const

    # ss_metric = ss.SchwarzschildMetric(
    #     M=const.M_earth,
    #     initial_vec_pos=[140, pi/2, 0],
    #     initial_vec_v=[0, 0, 1800]
    # )

    traj = ss_metric.calculate_trajectory(proptime_end=88 * 24 * 3600, step_size=1000)
    traj.plot(attractor_radius=6.9634e8)


if __name__ == "__main__":
    simple_trajectory()