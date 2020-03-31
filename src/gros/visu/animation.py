import plotly.graph_objects as go


def create_animation(dataset):
    axis_min = min([dataset["x"].min(), dataset["y"].min(), dataset["z"].min()])
    axis_max = max([dataset["x"].max(), dataset["y"].max(), dataset["z"].max()])

    x = dataset["x"]
    y = dataset["y"]
    z = dataset["z"]

    fig = go.Figure(
        data=[
            go.Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(width=2, color="blue")),
            go.Scatter3d(x=x, y=y, z=z, mode="lines", line=dict(width=2, color="blue")),
        ],
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
                    type="buttons",
                    buttons=[dict(label="Play", method="animate", args=[None])],
                )
            ],
        ),
        frames=[
            go.Frame(
                data=[
                    go.Scatter3d(
                        x=[x[k]],
                        y=[y[k]],
                        z=[z[k]],
                        mode="markers",
                        marker=dict(color="red", size=2),
                    )
                ]
            )
            for k in range(len(dataset.index))
        ],
    )

    return fig
