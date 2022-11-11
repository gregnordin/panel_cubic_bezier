# See https://discourse.holoviz.org/t/linking-tabulator-with-a-hv-plot/2377/4
import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np
import holoviews as hv

pn.extension("tabulator")  # , sizing_mode="stretch_width")


def append_row(df, din, point, dout):
    row = pd.Series([*din, *point, *dout], index=df.columns)
    return pd.concat([df, row.to_frame().T], ignore_index=True)


data_curves = dict(
    x_din=np.array([]),
    y_din=np.array([]),
    z_din=np.array([]),
    dx_p=np.array([]),
    dy_p=np.array([]),
    dz_p=np.array([]),
    x_dout=np.array([]),
    y_dout=np.array([]),
    z_dout=np.array([]),
)
df_data_curves = pd.DataFrame(data_curves)

din_start = [np.NaN, np.NaN, np.NaN]
point_start = [0, 0, 0]
dout_start = [2.0, 0, 0]

initial_curve_params = [
    [din_start, point_start, dout_start],
    [[2.0, 0.0, 0.0], [1.0, 1.0, 0.0], [1.0, 0.0, 0.0]],
    [[3.0, 0.0, 0.0], [1.0, -1.0, 0.0], [np.NaN, np.NaN, np.NaN]],
]

for row in initial_curve_params:
    df_data_curves = append_row(df_data_curves, *row)

point_info_tabulator = pn.widgets.Tabulator(value=df_data_curves, selectable=True)


def compute_plot(value):
    coords = [(value["dx_p"][i], value["dy_p"][i]) for i in range(len(value))]
    return hv.Scatter(coords)


plot = pn.bind(compute_plot, value=point_info_tabulator)

pn.Column(
    "# Point and Tangent info", "## Another level", point_info_tabulator, plot
).servable()  #

# pars = pd.DataFrame(
#     {"name": ["A", "B", "C"], "period": [1, 0.5, 0.3], "amplitude": [0.3, 0.4, 0.1]}
# )
# xx = np.linspace(0, 1, 100)


# def compute_plot(value):
#     arr = value["amplitude"].to_numpy() * np.sin(
#         np.outer(2 * np.pi * xx, 1.0 / value["period"].to_numpy())
#     )
#     curves = pd.DataFrame(
#         dict([(value["name"][i], arr[:, i]) for i in range(0, 3)]), index=xx
#     )
#     return curves.hvplot(grid=True)


# tabedit = pn.widgets.Tabulator(
#     value=pars, show_index=False, selectable=True, theme="site", height=140
# )
# plot = pn.bind(compute_plot, value=tabedit)

# pn.template.FastListTemplate(
#     site="Awesome Panel", title="Table Edits", main=[tabedit, plot]
# ).servable()
