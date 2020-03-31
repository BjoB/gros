#!/usr/bin/env python

from numpy import pi

from gros.metric import schwarzschild as ss
from gros.utils import const
from gros.utils import datahandling as dh
from gros.visu import animation


def simple_trajectory():
    # Initialize metric
    ss_metric = ss.SchwarzschildMetric(
        M=const.M_solar,
        initial_vec_pos=[10000000, pi/2, 0.3],
        initial_vec_v=[1000, 0, 0.08]
    )

    traj_data = dh.SpaceTimeData()
    for _, val in zip(range(100), ss_metric.generate_trajectory(step_size=1e-3)):
        print("tau = {}s, t = {}s, r = {}m, dt/dtau = {}".format(val[0], val[1][0], val[1][1], val[1][4]))
        traj_data.append(tau=val[0], vec=val[1])

    # TODO: ease API
    animation.create_animation(traj_data.df).show()


if __name__ == "__main__":
    simple_trajectory()
