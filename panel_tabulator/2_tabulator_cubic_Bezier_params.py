# See https://discourse.holoviz.org/t/linking-tabulator-with-a-hv-plot/2377/4
import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np
import holoviews as hv
import cubicbezier as bez

pn.extension("tabulator")  # , sizing_mode="stretch_width")


def compute_absolute_positions(value):
    return pd.DataFrame(
        [value["p_dx"].cumsum(), value["p_dy"].cumsum(), value["p_dz"].cumsum()]
    ).T.set_axis(["p_x", "p_y", "p_z"], axis=1)


def append_row(df, din, point, dout):
    row = pd.Series([*din, *point, *dout], index=df.columns)
    return pd.concat([df, row.to_frame().T], ignore_index=True)


data_curves = dict(
    din_x=np.array([]),
    din_y=np.array([]),
    din_z=np.array([]),
    p_dx=np.array([]),
    p_dy=np.array([]),
    p_dz=np.array([]),
    dout_x=np.array([]),
    dout_y=np.array([]),
    dout_z=np.array([]),
)
df_data_curves = pd.DataFrame(data_curves)

din_start = [np.NaN, np.NaN, np.NaN]
point_start = [0, 0, 0]
dout_start = [2.0, 0, 0]

initial_curve_params = [
    [din_start, point_start, dout_start],
    [[2.0, 0.0, 0.0], [1.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
    [[3.0, 0.0, 0.0], [1.0, -1.0, 0.0], [3.0, 0.0, 0.0]],
    [[-3.0, 0.0, 0.0], [0.0, 2.0, 0.0], [np.NaN, np.NaN, np.NaN]],
]

for row in initial_curve_params:
    df_data_curves = append_row(df_data_curves, *row)
point_info_tabulator = pn.widgets.Tabulator(value=df_data_curves, selectable=True)

plot_params = dict(
    x="x",
    y="y",
    xlabel="x",
    ylabel="y",
    # xlim=xlim,
    # ylim=ylim,
    # width=size_px,
    # height=size_px,
    legend="top",
    aspect="equal",
    width=400,
    height=400,
    xlim=(-3, 3),
    ylim=(-3, 3),
)
bezier_params = dict(
    line_width=5,
    grid=True,
)
colors = [
    "#1f77b4",
    "#ff7f0e",
    "#2ca02c",
    "#d62728",
    "#9467bd",
    "#8c564b",
    "#e377c2",
    "#7f7f7f",
    "#bcbd22",
    "#17becf",
]
color1 = colors[0]
color2 = colors[1]
color3 = colors[2]


def compute_plot(value):
    temp_df = compute_absolute_positions(value)
    points = np.array(
        [
            [temp_df["p_x"][i], temp_df["p_y"][i], temp_df["p_z"][i]]
            for i in range(len(temp_df))
        ]
    )
    din = np.array(
        [
            (value["din_x"][i], value["din_y"][i], value["din_z"][i])
            for i in range(len(value))
        ]
    )
    dout = np.array(
        [
            (value["dout_x"][i], value["dout_y"][i], value["dout_z"][i])
            for i in range(len(value))
        ]
    )
    bezier1 = bez.bezier_curve(p0=points[0], p1=points[1], d0=dout[0], d1=din[1])
    bezier2 = bez.bezier_curve(p0=points[1], p1=points[2], d0=dout[1], d1=din[2])
    bezier3 = bez.bezier_curve(p0=points[2], p1=points[3], d0=dout[2], d1=din[3])
    scatter = hv.Scatter(points).options(size=10, show_grid=True, color="#e377c2")
    cubic_bezier_line1 = bezier1.hvplot.line(
        **plot_params, **bezier_params, color=color1
    )
    cubic_bezier_line2 = bezier2.hvplot.line(
        **plot_params, **bezier_params, color=color2
    )
    cubic_bezier_line3 = bezier3.hvplot.line(
        **plot_params, **bezier_params, color=color3
    )
    return cubic_bezier_line1 * cubic_bezier_line2 * cubic_bezier_line3 * scatter


# df_bezier = bezier_curve(p0, p1, d0, d1)

plot = pn.bind(compute_plot, value=point_info_tabulator)
absolute_positions = pn.bind(compute_absolute_positions, value=point_info_tabulator)

pn.Column(
    """
    # Point and Tangent info
    p_dx,p_dy,p_dz &rarr; relative position from last point  
    din_x,din_y,din_z &rarr; tangent going into point  
    dout_x,dout_y,dout_z &rarr; tangent going out of point
    """,
    point_info_tabulator,
    "# Absolute Positions",
    absolute_positions,
    plot,
).servable()
