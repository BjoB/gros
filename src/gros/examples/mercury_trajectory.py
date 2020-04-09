#!/usr/bin/env python

from numpy import pi

from gros.metric import schwarzschild as ss
from gros.utils import const


def mercury_trajectory():

    # init metric with mass of sun and mercury orbit parameters
    ss_metric = ss.SchwarzschildMetric(
        M=const.M_solar,
        initial_vec_pos=[57.9e6 * 1000, pi/2, 0],
        initial_vec_v=[0, 0, (47.4 / 57.9e6)]
    )

    # TODO:
    # put proper time, coordinate time to plot and animation, singularity changes to red color when animating?
    # add different planet / black hole data to const

    radius_sun = 6.9634e8

    # calculate trajectory for one orbital period
    traj = ss_metric.calculate_trajectory(proptime_end=88 * 24 * 3600, step_size=3600)

    # animate with one frame per day
    traj.plot(attractor_radius=radius_sun, animation_step_size=24 * 3600)

    # comment out to show mercury's perihelion precession:
    # traj = ss_metric.calculate_trajectory(proptime_end=100 * 88 * 24 * 3600, step_size=86400)
    # traj.plot(attractor_radius=radius_sun)


if __name__ == "__main__":
    mercury_trajectory()
