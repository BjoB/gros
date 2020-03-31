import numpy as np

from gros.utils import datahandling as dh


def test_general_data_handling():
    traj_data = dh.SpaceTimeData()

    assert(traj_data.size() == 0)

    vec = np.array([1, 2, 3, 4, 5, 6, 7, 8])
    traj_data.append(tau=1.0, vec=vec)
    traj_data.append(tau=2.0, vec=vec)

    assert(traj_data.size() == 2)


test_general_data_handling()
