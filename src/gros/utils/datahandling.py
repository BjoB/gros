import math
import numpy as np
import pandas as pd
import plotly.graph_objects as go

from gros.utils import log, transforms as tf


logger = log.init_logger(__name__)
DATA_COLUMNS = ["tau", "t", "x", "y", "z"]


class SpaceTimeData:
    """
    Class for wrapping spacetime data points.
    """

    def __init__(
        self, trajectory, rs, conversion=tf.CoordinateConversion.spherical_to_cartesian
    ):
        """
        Initialize dataset of trajectory points.
        Arguments:
        rs -- Schwarzschild radius of center mass [m]
        """
        if not isinstance(trajectory, np.ndarray):
            raise ValueError("dataset must be numpy ndarray!")
        if trajectory.shape != (len(trajectory), 5):
            raise ValueError("dataset shape needs to be (N,5)!")

        self.rs = rs
        self.max_num_anim_frames = 100

        if trajectory.any():
            self.df = pd.DataFrame(trajectory, columns=DATA_COLUMNS)
            if conversion is tf.CoordinateConversion.spherical_to_cartesian:
                for traj_point in trajectory:
                    (
                        traj_point[2],
                        traj_point[3],
                        traj_point[4],
                    ) = tf.spherical_to_cartesian(
                        r=traj_point[2], theta=traj_point[3], phi=traj_point[4]
                    )

    def size(self):
        """
        Returns number of datapoints.
        """
        return len(self.df.index)

    def plot(self, attractor_radius=0, animation_step_size=0, theme="dark"):
        """
        Plots the provided data points in a 3D scatter plot.

        Arguments:
            attractor_radius {int} -- Adds an additional sphere with given radius [m] to the plot (default: {0})
            animation_step_size {int} -- step size [s] > 0 will create an according animation (default: {0})
            theme {str} -- Plotting theme (default: {"dark"})
        """
        TRAJ_COLOR = "skyblue"
        SINGULARITY_COLOR = "darkviolet"
        BLACK_HOLE_COLOR = "darkviolet"

        data = self.df

        axis_min = min([data["x"].min(), data["y"].min(), data["z"].min()])
        axis_max = max([data["x"].max(), data["y"].max(), data["z"].max()])

        x = data["x"]
        y = data["y"]
        z = data["z"]

        # create marker for singularity
        singularity = go.Scatter3d(
            x=[0],
            y=[0],
            z=[0],
            mode="markers",
            marker=dict(size=1, color=SINGULARITY_COLOR),
            text="singularity",
            name="singularity",
            hoverinfo="text",
        )

        # attractor sphere
        attractor = self._create_sphere(attractor_radius, "attractor", "yellow", 0.1)

        # black hole sphere at r=rs
        black_hole = self._create_sphere(self.rs, "black hole", BLACK_HOLE_COLOR, 0.2)

        # trajectory
        traj_plot = go.Scatter3d(
            x=x,
            y=y,
            z=z,
            text="trajectory",
            name="trajectory",
            mode="lines",
            line=dict(width=2, color=TRAJ_COLOR),
        )

        plot_data = [
            go.Scatter3d(name="dummy"),
            singularity,
            black_hole,
            attractor,
            traj_plot,
        ]

        fig = go.Figure(
            data=plot_data,
            layout=go.Layout(
                scene=dict(
                    xaxis=dict(range=[axis_min, axis_max],),
                    yaxis=dict(range=[axis_min, axis_max],),
                    zaxis=dict(range=[axis_min, axis_max],),
                ),
                title_text="Particle orbit in gravitational field",
                hovermode="closest",
                updatemenus=[],
            ),
        )

        self._add_aninmation_frames(fig, animation_step_size)

        if theme == "dark":
            fig.update_layout(template="plotly_dark")
        fig.show()

    def _create_sphere(self, radius, name, color, opacity):
        sph_theta = np.linspace(0, 2 * np.pi)
        sph_phi = np.linspace(0, 2 * np.pi)
        sph_theta, sph_phi = np.meshgrid(sph_phi, sph_theta)

        sph_x, sph_y, sph_z = tf.spherical_to_cartesian(radius, sph_theta, sph_phi)

        sphere = go.Mesh3d(
            x=sph_x.flatten(),
            y=sph_y.flatten(),
            z=sph_z.flatten(),
            alphahull=0,
            opacity=opacity,
            color=color,
            text=name,
            name=name,
        )

        return sphere

    def _add_aninmation_frames(self, fig, anim_step_size):
        """Adds animation frames with given (index) step size to the figure.

        Arguments:
            fig -- plotly figure
            anim_step_size -- animation step size [s]
        """
        if anim_step_size <= 0:
            return

        # buttons
        updatemenus_dict = {
            # "bgcolor": "#333333",
            "font": {"color": "#000000"},
            "type": "buttons",
            "buttons": [
                {
                    "label": "Play",
                    "method": "animate",
                    "args": [
                        None,
                        {
                            "frame": {"duration": 500, "redraw": True},
                            "fromcurrent": True,
                            "transition": {
                                "duration": 300,
                                "easing": "quadratic-in-out",
                            },
                        },
                    ],
                },
                {
                    "label": "Pause",
                    "method": "animate",
                    "args": [
                        [None],
                        {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0},
                        },
                    ],
                },
            ],
            "showactive": False,
        }

        # animation frame traits
        frame_step_size = math.ceil(anim_step_size / self.df["tau"].max() * self.size())

        if frame_step_size > self.max_num_anim_frames:
            frame_step_size = self.max_num_anim_frames
            logger.warning(
                "'animation_step_size' is too large. \
                    Maximium number of animation frames will be limited to {}.".format(
                    self.max_num_anim_frames
                )
            )
        anim_frame_range = list(range(1, self.size(), frame_step_size))

        # sliders
        sliders_dict = {
            "active": 0,
            "yanchor": "top",
            "xanchor": "left",
            "currentvalue": {
                "font": {"size": 12},
                "prefix": "t[s]=",
                "visible": True,
                "xanchor": "right",
            },
            "transition": {"duration": 300, "easing": "cubic-in-out"},
            "pad": {"b": 10, "t": 50},
            "len": 0.9,
            "x": 0.1,
            "y": 0,
            "steps": [],
        }

        # append frames and slider steps
        anim_frames = []
        for k in anim_frame_range:
            current_tau = self.df["tau"][k]

            frame = go.Frame(
                data=[
                    go.Scatter3d(
                        x=[self.df["x"][k]],
                        y=[self.df["y"][k]],
                        z=[self.df["z"][k]],
                        mode="markers",
                        marker=dict(color="red", size=3),
                        name="particle",
                        text="particle",
                    )
                ],
                name=str(current_tau),
            )
            anim_frames.append(frame)

            slider_step = {
                "args": [
                    [str(current_tau)],
                    {
                        "frame": {"duration": 300, "redraw": True},
                        "mode": "immediate",
                        "transition": {"duration": 300},
                    },
                ],
                "label": current_tau,
                "method": "animate",
            }
            sliders_dict["steps"].append(slider_step)

        # update figure data
        fig.frames = anim_frames
        fig.update_layout(updatemenus=[updatemenus_dict], sliders=[sliders_dict])
