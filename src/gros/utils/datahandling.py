import numpy as np
import pandas as pd

from gros.utils import log, transforms as tf


logger = log.init_logger(__name__)
data_columns = ["tau", "t", "x", "y", "z"]


class SpaceTimeData:
    """
    Class for wrapping spacetime data points.
    """

    def __init__(self, dataset=None):
        """
        Initialize dataset as empty dataframe or fill with provided data.
        """

        if dataset:
            # TODO: not supported yet
            assert("The dataset feature is not yet supported!")
            self.df = pd.DataFrame(dataset, columns=data_columns)
        else:
            self.df = pd.DataFrame(columns=data_columns)

    def size(self):
        """
        Returns current number of datapoints.
        """
        return len(self.df.index)

    def append(self, tau, vec, coord_system=tf.CoordinateSystem.spherical):
        """
        Appends new spacetime datapoint.

        Arguments:
            tau -- proper time [s]
            vec -- spacetime point with velocities as numpy array of shape (8,)
            coord_system -- coordinate system of provided vec
        """
        if not isinstance(vec, np.ndarray) or vec.shape != (8,):
            logger.error("data point must be numpy array of shape (8,)!")
            return

        x, y, z, vx, vy, vz = tf.spherical_to_cartesian(
            r=vec[1], theta=vec[2], phi=vec[3], v_r=vec[5], v_theta=vec[6], v_phi=vec[7]
        )

        self.df = self.df.append(
            {
                data_columns[0]: tau,
                data_columns[1]: vec[0],
                data_columns[2]: x,
                data_columns[3]: y,
                data_columns[4]: z,
            },
            ignore_index=True,
        )
