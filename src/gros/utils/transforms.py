import numpy as np
from enum import Enum


class CoordinateSystem(Enum):
    cartesian = 1
    spherical = 2


class CoordinateConversion(Enum):
    spherical_to_cartesian = 1
    cartesian_to_spherical = 2


def spherical_to_cartesian(r, theta, phi):
    """Transforms coordinates from spherical to cartesian.

    Returns:
        cartesian coordinates
    """
    x = r * np.sin(theta) * np.cos(phi)
    y = r * np.sin(theta) * np.sin(phi)
    z = r * np.cos(theta)

    return x, y, z


def spherical_to_cartesian_with_vel(r, theta, phi, v_r, v_theta, v_phi):
    """Transforms coordinates and according velocities from spherical to cartesian.

    Returns:
        cartesian coordinates and velocities
    """
    x, y, z = spherical_to_cartesian(r, theta, phi)

    v_x = (
        np.sin(theta) * np.cos(phi) * v_r
        - r * np.sin(theta) * np.sin(phi) * v_phi
        + r * np.cos(theta) * np.cos(phi) * v_theta
    )
    v_y = (
        np.sin(theta) * np.sin(phi) * v_r
        + r * np.cos(theta) * np.sin(phi) * v_theta
        + r * np.sin(theta) * np.cos(phi) * v_phi
    )
    v_z = np.cos(theta) * v_r - r * np.sin(theta) * v_theta

    return x, y, z, v_x, v_y, v_z
