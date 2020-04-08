import numpy as np

from gros.utils import datahandling as dh


def test_general_data_handling():
    testdata = np.array([
        [0, 0, 1, 2, 3],
        [1, 1, 4, 5, 6]
    ])
    traj_data = dh.SpaceTimeData(testdata, 1000)
    assert(traj_data.size() == 2)


test_general_data_handling()
