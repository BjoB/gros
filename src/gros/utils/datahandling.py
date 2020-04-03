import numpy as np
import pandas as pd
import plotly.graph_objects as go

from gros.utils import transforms as tf


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

    def plot(self, attractor_radius=0, theme="dark"):
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

        # trajectories (plot + animation)
        traj1 = go.Scatter3d(
            x=x,
            y=y,
            z=z,
            text="trajectory",
            name="trajectory",
            mode="lines",
            line=dict(width=2, color=TRAJ_COLOR),
        )
        traj2 = go.Scatter3d(
            x=x,
            y=y,
            z=z,
            text="trajectory",
            name="trajectory",
            mode="lines",
            line=dict(width=2, color=TRAJ_COLOR),
        )

        fig = go.Figure(
            data=[singularity, black_hole, attractor, traj1, traj2],
            layout=go.Layout(
                scene=dict(
                    xaxis=dict(range=[axis_min, axis_max],),
                    yaxis=dict(range=[axis_min, axis_max],),
                    zaxis=dict(range=[axis_min, axis_max],),
                ),
                title_text="Particle curve in gravitational field",
                hovermode="closest",
                updatemenus=[
                    dict(
                        # bgcolor="#333333",
                        font=dict(color="#000000"),
                        type="buttons",
                        buttons=[dict(label="Play", method="animate", args=[])],
                    )
                ],
            ),
            # frames=[
            #     go.Frame(
            #         data=[
            #             go.Scatter3d(
            #                 x=[x[k]],
            #                 y=[y[k]],
            #                 z=[z[k]],
            #                 mode="markers",
            #                 marker=dict(color="red", size=4),
            #             )
            #         ]
            #     )
            #     for k in range(len(data.index))
            # ],
        )

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
