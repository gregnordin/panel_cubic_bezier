import numpy as np
import pandas as pd
import panel as pn

import hvplot.pandas
import holoviews as hv

pn.extension(sizing_mode="stretch_width")

# -------------------------------------------------------------------------------------------
# Utilities
# -------------------------------------------------------------------------------------------


def arrowhead(p0, p1, length=0.15, arrow_angle_deg=25):
    """Calculate arrowhead points. This is formulated for 2D only.
    See `notes_to_self/python/holoviz/221103_HoloViz_draw_own_arrowheads.ipynb`.
    """
    # See https://math.stackexchange.com/questions/2051149/how-to-draw-arrowheads

    w = length * np.cos(
        np.deg2rad(arrow_angle_deg)
    )  # Arrowhead length in direction of line
    h = length * np.sin(
        np.deg2rad(arrow_angle_deg)
    )  # Arrowhead length orthogonal to line
    n_hat = (p1 - p0) / np.linalg.norm(p1 - p0)  # Unit vector in direction of line
    c_hat = np.array([n_hat[1], -n_hat[0]])  # Unit vector orthogonal to line

    # Arrowhead endpoints
    pa = p1 - w * n_hat - h * c_hat
    pb = p1 - w * n_hat + h * c_hat

    # Gather into x and y components
    px = np.array([pa[0], p1[0], pb[0]])  # , pa[0]])
    py = np.array([pa[1], p1[1], pb[1]])  # , pa[1]])

    return dict(x=px, y=py)


def show_head_and_tail(df, nrows=5):
    """See https://www.askpython.com/python-modules/pandas/head-and-tail-of-dataframe-series"""
    with pd.option_context("display.max_rows", 2 * nrows):
        print(df)


def make_data_df(a, b):
    return dict(
        x=[a[0], b[0]],
        y=[a[1], b[1]],
        z=[a[2], b[2]],
    )


def make_single_point_data_df(p):
    return dict(
        x=[p[0]],
        y=[p[1]],
        z=[p[2]],
    )


def make_tangent_data_df(a, b):
    p = a + b
    return dict(
        x=[a[0], p[0]],
        y=[a[1], p[1]],
        z=[a[2], p[2]],
    )


def hv_unit_circle(
    x0=0,
    y0=0,
    n_segments=100,
    fill_color="lightgray",
    line_color=None,
    alpha=0.3,
    aspect="equal",
):
    angles = np.linspace(0, 2 * np.pi, num=n_segments, endpoint=False)
    circle_polygon_data = dict(
        x=x0 + np.cos(angles),
        y=y0 + np.sin(angles),
    )
    return hv.Polygons(circle_polygon_data).options(
        fill_color=fill_color, line_color=line_color, alpha=alpha, aspect=aspect
    )


# -------------------------------------------------------------------------------------------
# Cubic Bezier curve functions
# -------------------------------------------------------------------------------------------


def p(t, c0, c1, c2, c3):
    """Cubic 3D Bezier curve."""
    t0 = (1 - t) ** 3
    t1 = 3 * t * (1 - t) ** 2
    t2 = 3 * (t**2) * (1 - t)
    t3 = t**3
    # print(t0, t1, t2, t3)
    return t0 * c0 + t1 * c1 + t2 * c2 + t3 * c3


def dp(t, c0, c1, c2, c3):
    """Derivative of cubic 3D Bezier curve -> tangent at point for value of t."""
    a0 = -3 * c0 * (1 - t) ** 2
    a1 = 3 * c1 * (t * (2 * t - 2) + (1 - t) ** 2)
    a2 = 3 * c2 * (-1 * t**2 + 2 * t * (1 - t))
    a3 = 3 * c3 * t**2
    return a0 + a1 + a2 + a3


tt = np.linspace(0, 1, 101)


def bezier_curve(p0, p1, d0, d1, tt=tt):

    c0 = p0
    c1 = p0 + d0 / 3.0
    c2 = p1 - d1 / 3.0
    c3 = p1

    pt = np.array([p(t, c0, c1, c2, c3) for t in tt])

    df = pd.DataFrame(
        np.array([tt, pt[:, 0], pt[:, 1], pt[:, 2]]).T, columns=["t", "x", "y", "z"]
    )
    return df


def make_tangent_df(point, tangent):
    df = pd.DataFrame(np.array([point, point + tangent]), columns=["x", "y", "z"])
    df["marker"] = ["circle", "diamond"]
    df["marker_size"] = [50, 150]
    return df


# Example:
# make_tangent_df(np.array([0, 0, 0]), np.array([5, 1, 0]))
# 	x	y	z	marker	marker_size
# 0	0	0	0	circle	50
# 1	5	1	0	diamond	150

# Initialize overall parameters
size_px = 600
xlim = (-3, 3)
ylim = xlim
plot_params = dict(
    x="x",
    y="y",
    xlabel="x",
    ylabel="y",
    xlim=xlim,
    ylim=ylim,
    width=size_px,
    height=size_px,
    legend="top",
)
bezier_params = dict(
    line_width=5,
    grid=True,
)

# Initialize tangent line parameters
d0_color = "red"
d1_color = "green"
tangent_scatter_params = dict(
    marker="marker",
    size="marker_size",
    line_alpha=0.5,
)
tangent_line_params = dict(
    line_alpha=0.5,
)

# Interactive Bezier curve
p1_angle_deg_slider = pn.widgets.IntSlider(
    name="Angle from x-axis (deg)", start=-180, end=180, value=45
)
d0_length_slider = pn.widgets.FloatSlider(name="Length", start=0.1, end=5.0, value=2.0)
d0_angle_deg_slider = pn.widgets.IntSlider(
    name="Angle from x-axis (deg)", start=-180, end=180, value=0
)
d1_length_slider = pn.widgets.FloatSlider(name="Length", start=0.1, end=5.0, value=2.0)
d1_angle_deg_slider = pn.widgets.IntSlider(
    name="Angle from x-axis (deg)", start=-180, end=180, value=0
)


def bezier_curve_bind(
    p1_angle_deg, d0_length, d0_angle_deg, d1_length, d1_angle_deg, tt=tt
):
    p0 = np.array([0, 0, 0])
    p1 = np.array(
        [np.cos(np.deg2rad(p1_angle_deg)), np.sin(np.deg2rad(p1_angle_deg)), 0]
    )
    d0 = d0_length * np.array(
        [np.cos(np.deg2rad(d0_angle_deg)), np.sin(np.deg2rad(d0_angle_deg)), 0]
    )
    d1 = d1_length * np.array(
        [np.cos(np.deg2rad(d1_angle_deg)), np.sin(np.deg2rad(d1_angle_deg)), 0]
    )

    df_bezier = bezier_curve(p0, p1, d0, d1)
    df_d0 = make_tangent_df(p0, d0)
    df_d1 = make_tangent_df(p1, d1)

    cubic_bezier_line = df_bezier.hvplot.line(**plot_params, **bezier_params)
    tangent_line_params = dict(
        line_alpha=0.5,
    )
    d0_line = hv.Curve(df_d0).options(
        line_dash="dashed", color=d0_color, **tangent_line_params
    ) * hv.Curve(arrowhead(p0[:2], d0[:2])).options(
        aspect="equal", color=d0_color, **tangent_line_params
    )
    d1_line = hv.Curve(df_d1).options(
        line_dash="dashed", color=d1_color, **tangent_line_params
    ) * hv.Curve(arrowhead(p1[:2], p1[:2] + d1[:2])).options(
        aspect="equal", color=d1_color, **tangent_line_params
    )
    p_points_params = dict(
        size=10,
        alpha=0.5,
    )
    p_points = hv.Scatter(make_single_point_data_df(p0)).options(
        **p_points_params, color=d0_color
    ) * hv.Scatter(make_single_point_data_df(p1)).options(
        **p_points_params, color=d1_color
    )

    # tangents = d0_line * d1_line * p_points

    return hv_unit_circle() * cubic_bezier_line * d0_line * d1_line * p_points


interactive_bezier = pn.bind(
    bezier_curve_bind,
    p1_angle_deg_slider,
    d0_length_slider,
    d0_angle_deg_slider,
    d1_length_slider,
    d1_angle_deg_slider,
)

template = pn.template.FastListTemplate(
    title="Interactive Cubic Bezier Curve",
    sidebar=[
        "## Start: Origin",
        "## End: Point on unit circle",
        p1_angle_deg_slider,
        pn.layout.Divider(),
        "## Tangent at start point",
        d0_angle_deg_slider,
        d0_length_slider,
        pn.layout.Divider(),
        "## Tangent at end point",
        d1_angle_deg_slider,
        d1_length_slider,
    ],
    main=[interactive_bezier],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
)
template.servable()
