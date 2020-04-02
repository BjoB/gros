from gros.metric import schwarzschild as ss
from gros.utils import const
from numpy import pi
from numpy import sqrt


def calc_schwarzschild_trajectory():
    r = 140000000000

    ss_metric = ss.SchwarzschildMetric(
        M=const.M_solar,
        initial_vec_pos=[r, pi/2, 0.3],
        initial_vec_v=[1000, 0.0, 0.0]
    )

    for val in ss_metric.trajectory_generator(proptime_end=100, step_size=1):
        print("tau = {}s, t = {}s, r = {}m, dt/dtau = {}".format(val[0], val[1][0], val[1][1], val[1][4]))

    dt_factor = 1/sqrt(1 - ss_metric.schwarzschild_radius() / r)
    print("theoretical dt/dtau = {}".format(dt_factor))


calc_schwarzschild_trajectory()
