from gros.metric import schwarzschild as ss
from gros.utils import const
from numpy import pi
from numpy import sqrt


def calc_schwarzschild_trajectory():
    r = 3400

    ss_metric = ss.SchwarzschildMetric(
        M=const.M_solar,
        initial_vec_pos=[r, pi/2, 0.3],
        initial_vec_v=[0.0, 0.0, 0.0]
    )

    for _, val in zip(range(5000), ss_metric.generate_trajectory()):
        print("tau = {}s, t = {}s, r = {}m, dt/dtau = {}".format(val[0], val[1][0], val[1][1], val[1][4]))

    dt_factor = 1/sqrt(1 - ss.calc_schwarzschild_radius(const.M_solar).value / r)
    print("theoretical dt/dtau = {}".format(dt_factor))


calc_schwarzschild_trajectory()
