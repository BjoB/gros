import numpy as np


def spherical_to_cartesian(r, theta, phi, v_r, v_theta, v_phi):
    """Transforms coordinates and velocity from spherical to cartesian.

    Returns:
        cartesian coordinates and velocities
    """
    x = r * np.cos(phi) * np.sin(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(theta)

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
