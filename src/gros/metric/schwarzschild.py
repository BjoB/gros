import numpy as np

from astropy import units as u
from scipy import integrate

from gros.utils import const


class SchwarzschildMetric():
    """
    Class for calculations with the Schwarschild metric,
    e.g. for solving the geodesic equation for an orbiting object.

    Note: See following lecture notes as an overview of the used formulas:
    http://www.physics.usu.edu/Wheeler/GenRel/Lectures/GRNotesDecSchwarzschildGeodesicsPost.pdf
    """

    @u.quantity_input(M=u.kg, time=u.s)
    def __init__(self, M=u.kg, initial_vec_pos, initial_vec_v, time=0):
        """
        Initializes a Schwarzschild metric with given mass,
        start time and spatial coordinates and velocities.

        Arguments:
            M -- mass of gravitational center [kg]
            initial_vec_pos -- initial spherical coordinates [r[m], theta[rad], phi[rad]]
            sperical_velos -- initial spherical velocities [r', theta', phi']
            time -- initial time [s]
        """
        self.M = M.value
        self.a = -1 * calc_schwarzschild_radius(M).value

        self.initial_vec_x_u = np.hstack(
            (
                time.value,
                initial_vec_pos,
                self._calc_initial_dt_dtau(initial_vec_pos, initial_vec_v),
                initial_vec_v
            )
        )

    def calc_trajectory_iterator(self, proper_time=0):
        """
        Iterator for solving the next time step of the geodesic's ODE system.

        Arguments:
            proper_time -- start proper time [s]

        Yields:
            proper time,
            vector composed of the updated 4-vector and 4-velocity
            => [t, r, theta, phi, dt/dtau, dr/dtau, dtheta/dtau, dphi/dtau]
        """
        ode_solver = integrate.RK45(
            self._calc_next_velo_and_acc_vec,
            t0=proper_time,
            y0=self.initial_vec_x_u,
            t_bound=1e100,
        )
        ode_solver.step_size(1e-3)

        while True:
            yield ode_solver.t, ode_solver.y
            ode_solver.step()

    def _calc_christoffel_symbols(self, r, theta, c=const.c.value, G=const.G.value):
        """
        Calculate the Christoffel symbols for the initialized mass
        at the coordinates r, theta.

        Arguments:
            r -- radius in m
            theta -- angle in radians (z-axis)

        Returns:
            Christoffel symbols as (4,4,4) numpy array
        """
        a = self.a.value
        r2 = r**2
        a_div_r = a/r
        chrs = np.zeros(shape=(4, 4, 4), dtype=float)

        chrs[0, 0, 1] = chrs[0, 1, 0] = -0.5 * a / (r2 * (1 + a_div_r))
        chrs[1, 0, 0] = -0.5 * (1 + a_div_r) * a_div_r / r * c ** 2
        chrs[1, 1, 1] = -chrs[0, 0, 1]
        chrs[2, 1, 2] = chrs[2, 2, 1] = 1 / r
        chrs[1, 2, 2] = a - r
        chrs[3, 1, 3] = chrs[3, 3, 1] = chrs[2, 1, 2]
        chrs[1, 3, 3] = (a - r) * (np.sin(theta) ** 2)
        chrs[3, 2, 3] = chrs[3, 3, 2] = 1 / np.tan(theta)
        chrs[2, 3, 3] = np.sin(theta) * np.cos(theta)
        return chrs

    def _calc_initial_dt_dtau(self, vec_pos, vec_v):
        """
        Calculates the initial time velocity dt/dtau.

        Arguments:
            vec_pos -- spatial part of four-vector (r, theta, phi)
            vec_v -- spatial part of four-velocity (dr/dtau, dtheta/dtau, dphi/dtau)

        Returns:
            Initial time velocity dt/dtau
        """
        a, c = self.a, const.c.value
        c2 = c ** 2

        temp1 = (1 / (c2 * (1 + a / vec_pos[0]))) * (vec_v[0] ** 2)
        temp2 = ((vec_pos[0] ** 2) / c2) * (vec_v[1] ** 2)
        temp3 = (vec_pos[0] ** 2) / (c ** 2) * (np.sin(vec_pos[1]) ** 2) * (vec_v[2] ** 2)
        dt_dtau_squared = (1 + temp1 + temp2 + temp3) / (1 + a / vec_pos[0])
        return np.sqrt(dt_dtau_squared) * u.one

    def _calc_next_velo_and_acc_vec(self, vec_x_u):
        """
        Calculates the acceleration components u' of a particle in the gravitational field
        based on the current position (four-vector x) and the corresponding four-velocity u.

        Arguments:
            vec_x_u -- combined four-vector x and four-velocity u
                       => [x, u] = [t, r, theta, phi, dt/dtau, dr/dtau, dtheta/dtau, dphi/dtau]
        Returns:
            8-component-vector, composed of the derivatives of the input vector
            => [u, u']
        """
        derivs = np.zeros(shape=vec_x_u.shape, dtype=vec_x_u.dtype)
        chs = self.calc_christoffel_symbols(vec_x_u[1], vec_x_u[2], self.M.value)

        derivs[:4] = vec_x_u[4:8]
        derivs[4] = -2 * chs[0, 0, 1] * vec_x_u[4] * vec_x_u[5]
        derivs[5] = -1 * (chs[1, 0, 0] * (vec_x_u[4] ** 2) + chs[1, 1, 1] * (vec_x_u[5] ** 2) \
                    + chs[1, 2, 2] * (vec_x_u[6] ** 2) + chs[1, 3, 3] * (vec_x_u[7] ** 2)
        derivs[6] = -2 * chs[2, 2, 1] * vec_x_u[6] * vec_x_u[5] - chs[2, 3, 3] * (vec_x_u[7] ** 2)
        derivs[7] = -2 * (chs[3, 1, 3] * vec_x_u[5] * vec_x_u[7] + chs[3, 2, 3] * vec_x_u[6] * vec_x_u[7])
        return derivs


@u.quantity_input(M=u.kg)
def calc_schwarzschild_radius(M=u.kg):
    """
    Calculates the Schwarzschild radius of a point mass M,
    which defines the event horizon of a Schwarzschild black hole.

    Arguments:
        M -- mass in kg

    Returns:
        Schwarzschild radius in meter
    """
    return (2 * const.G * M / (const.c ** 2))


if __name__ == "__main__":
    ss = SchwarzschildMetric(1000, [1,2,3], [1,2,3])
