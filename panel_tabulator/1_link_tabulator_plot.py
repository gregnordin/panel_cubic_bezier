# See https://discourse.holoviz.org/t/linking-tabulator-with-a-hv-plot/2377/4
import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np

pn.extension("tabulator")  # , sizing_mode="stretch_width")

lookup = {0: "A", 1: "B", 2: "C"}

pars = pd.DataFrame(
    {"name": ["A", "B", "C"], "period": [1, 0.5, 0.3], "amplitude": [0.3, 0.4, 0.1]}
)
xx = np.linspace(0, 1, 100)


def compute_plot(value):
    arr = value["amplitude"].to_numpy() * np.sin(
        np.outer(2 * np.pi * xx, 1.0 / value["period"].to_numpy())
    )
    curves = pd.DataFrame(
        dict([(value["name"][i], arr[:, i]) for i in range(0, 3)]), index=xx
    )
    return curves.hvplot(grid=True)


tabedit = pn.widgets.Tabulator(
    value=pars, show_index=False, selectable=True, theme="site", height=140
)
plot = pn.bind(compute_plot, value=tabedit)

pn.template.FastListTemplate(
    site="Awesome Panel", title="Table Edits", main=[tabedit, plot]
).servable()
