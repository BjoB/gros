from gros.metric import SchwarzschildMetric
from gros.utils import const


def calc_schwarzschild_trajectory():
    ss_metric = SchwarzschildMetric(
        M=const.M_solar,
        initial_vec_pos=[1e6, 0, 0],
        initial_vec_v=[1e3, 0.001, 0]
    )

    ss_metric.calc_trajectory_iterator()
