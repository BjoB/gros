import numpy as np
from astropy import units as u
from scipy import integrate

from gros.utils import const, log, datahandling as dh


logger = log.init_logger(__name__)


class SchwarzschildMetric:
    """
    Class for calculations with the Schwarschild metric,
    e.g. for solving the geodesic equation for an orbiting object.

    Note: See following lecture notes for a deeper look into the used formulas:
    https://web.stanford.edu/~oas/SI/SRGR/notes/SchwarzschildSolution.pdf
    https://arxiv.org/pdf/0904.4184.pdf
    http://www.physics.usu.edu/Wheeler/GenRel/Lectures/GRNotesDecSchwarzschildGeodesicsPost.pdf
    """

    @u.quantity_input(M=u.kg, time=u.s)
    def __init__(self, M, initial_vec_pos, initial_vec_v, time=0 * u.s):
        """
        Initializes a Schwarzschild metric with given mass,
        start time and spatial coordinates and velocities of a test particle.

        Arguments:
            M -- mass of gravitational center [kg]
            initial_vec_pos -- initial spherical coordinates [r[m], theta[rad], phi[rad]]
            sperical_velos -- initial spherical velocities [r', theta', phi']
            time -- initial time [s]
        """
        self.M = M.value
        self.rs = calc_schwarzschild_radius(M).value
        self.a = -self.rs

        logger.info("Event horizon for given mass is at r={}m.".format(self.rs))

        self.initial_vec_x_u = np.hstack(
            (
                time.value,
                initial_vec_pos,
                self._calc_initial_dt_dtau(initial_vec_pos, initial_vec_v),
                initial_vec_v,
            )
        )

    def schwarzschild_radius(self):
        """
        Returns the Schwarzschild radius for the initialized mass.
        """
        return self.rs

    def calculate_trajectory(self, proptime_end, proptime_start=0, step_size=1e-3):
        """
        Solve geodesic equations for provided time interval.

        Arguments:
            proptime_end -- end of interval [s]
            proptime_start -- start of inteval [s]
            step_size -- step size [s]

        Returns:
            (N,9) numpy ndarray with N = number of interations,
            single row is [tau, t, x, y, z]
        """
        tau = []
        y = []

        for cur_tau, cur_val in self.trajectory_generator(
            proptime_end=proptime_end,
            proptime_start=proptime_start,
            step_size=step_size,
        ):
            tau.append(cur_tau), y.append(cur_val)

            logger.debug(
                "tau={tau}s, t={t}s, r={r}m, dt/dtau={dtdtau}".format(
                    tau=cur_tau, t=cur_val[0], r=cur_val[1], dtdtau=cur_val[4]
                )
            )

        np_tau = np.reshape(tau, (len(tau), 1))
        np_y = np.array(y)

        # only extract rows for [tau, t, x, y, z]
        return dh.SpaceTimeData(np.hstack((np_tau, np_y[:, [0, 1, 2, 3]])), self.rs)

    def trajectory_generator(self, proptime_end, proptime_start=0, step_size=1e-3):
        """
        Generator for solving the next time step of the geodesic's ODE system.

        Arguments:
            proptime_end -- end of interval [s]
            proptime_start -- start proper time [s]
            step_size -- step size [s]

        Yields:
            proper time,
            vector composed of the updated 4-vector and 4-velocity
            => [t, r, theta, phi, dt/dtau, dr/dtau, dtheta/dtau, dphi/dtau]
        """
        ode_solver = integrate.RK45(
            self._calc_next_velo_and_acc_vec,
            t0=proptime_start,
            y0=self.initial_vec_x_u,
            t_bound=1e100,
            rtol=0.25 * step_size,
            first_step=0.75 * step_size,
            max_step=5 * step_size,
        )

        while True:
            yield ode_solver.t, ode_solver.y
            ode_solver.step()

            current_radius = ode_solver.y[1]
            rs = -self.a
            rs_border = rs * 1.01

            if ode_solver.t >= proptime_end:
                break

            if current_radius <= rs_border:
                logger.warning(
                    "Nearly reached event horizon at r={}m. Stopping here!".format(rs)
                )
                break

    def _calc_christoffel_symbols(self, r, theta):
        """
        Calculate the Christoffel symbols for the initialized mass
        at the coordinates r, theta.

        Arguments:
            r -- radius in m
            theta -- angle in radians (z-axis)

        Returns:
            Christoffel symbols as (4,4,4) numpy array
        """
        a = self.a
        a_div_r = a / r
        chrs = np.zeros(shape=(4, 4, 4), dtype=float)

        chrs[0, 0, 1] = chrs[0, 1, 0] = -0.5 * a / ((r ** 2) * (1 + a_div_r))
        chrs[1, 0, 0] = -0.5 * (1 + a_div_r) * (const.c.value ** 2) * a_div_r / r
        chrs[1, 1, 1] = -chrs[0, 0, 1]
        chrs[2, 1, 2] = chrs[2, 2, 1] = 1 / r
        chrs[1, 2, 2] = -1 * (r + a)
        chrs[3, 1, 3] = chrs[3, 3, 1] = chrs[2, 1, 2]
        chrs[1, 3, 3] = -1 * (r + a) * (np.sin(theta) ** 2)
        chrs[3, 2, 3] = chrs[3, 3, 2] = 1 / np.tan(theta)
        chrs[2, 3, 3] = -1 * np.sin(theta) * np.cos(theta)
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
        temp3 = (vec_pos[0] ** 2) / c2 * (np.sin(vec_pos[1]) ** 2) * (vec_v[2] ** 2)
        dt_dtau_squared = (1 + temp1 + temp2 + temp3) / (1 + a / vec_pos[0])
        return np.sqrt(dt_dtau_squared)

    def _calc_next_velo_and_acc_vec(self, proper_time, vec_x_u):
        """
        Calculates the acceleration components u' of a particle in the gravitational field
        based on the current position (four-vector x) and the corresponding four-velocity u.

        Arguments:
            vec_x_u -- combined four-vector x and four-velocity u,
                       [x, u] = [t, r, theta, phi, dt/dtau, dr/dtau, dtheta/dtau, dphi/dtau]
        Returns:
            8-component-vector [u, u'], composed of the derivatives of the input vector
        """
        derivs = np.zeros(shape=vec_x_u.shape, dtype=vec_x_u.dtype)
        chs = self._calc_christoffel_symbols(r=vec_x_u[1], theta=vec_x_u[2])

        derivs[:4] = vec_x_u[4:8]
        derivs[4] = -2 * chs[0, 0, 1] * vec_x_u[4] * vec_x_u[5]
        derivs[5] = -1 * (
            chs[1, 0, 0] * (vec_x_u[4] ** 2)
            + chs[1, 1, 1] * (vec_x_u[5] ** 2)
            + chs[1, 2, 2] * (vec_x_u[6] ** 2)
            + chs[1, 3, 3] * (vec_x_u[7] ** 2)
        )
        derivs[6] = -2 * chs[2, 2, 1] * vec_x_u[6] * vec_x_u[5] - chs[2, 3, 3] * (
            vec_x_u[7] ** 2
        )
        derivs[7] = -2 * (
            chs[3, 1, 3] * vec_x_u[5] * vec_x_u[7]
            + chs[3, 2, 3] * vec_x_u[6] * vec_x_u[7]
        )

        return derivs


# TODO:
# class Geodesic(SchwarzschildMetric):
#     """[summary]

#     Arguments:
#         SchwarzschildMetric {[type]} -- [description]
#     """
#     @u.quantity_input(M=u.kg, stop_time=u.s, start_time=u.s)
#     def __init__(self, M, initial_vec_pos, initial_vec_v, stop_time, start_time=0 * u.s):
#         super.__init__(M, initial_vec_pos, initial_vec_v, start_time)


@u.quantity_input(M=u.kg)
def calc_schwarzschild_radius(M=u.kg):
    """
    Calculates the Schwarzschild radius of a point mass M,
    which defines the event horizon of a Schwarzschild black hole.

    Arguments:
        M -- mass [kg]

    Returns:
        Schwarzschild radius [m]
    """
    return 2 * const.G * M / (const.c ** 2)
