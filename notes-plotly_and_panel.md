# Install and set up
```
#---------------------------------------------
# These are the commands that worked
#---------------------------------------------

# Create new conda env with python 3.10
conda create --name try_panel python=3.10 
# Activate it
conda activate try_panel
# Install version of plotly that supports 3D line plots
conda install -c plotly plotly=5.11.0
# Install all of the other stuff I will need to do panel stuff
conda install -c conda-forge hvplot panel pandas jupyterlab jupyter-panel-proxy jupyter_bokeh

# Install the following in `jupyter_py39` to hopefully enable plotly to work in jupyter lab
jupyter labextension install jupyterlab-plotly
# This step took a long time.

# Start jupyter lab from `jupyter_py39` and execute the following with the `try_panel` kernel and it should work:

import plotly.express as px
fig = px.bar(x=["a", "b", "c"], y=[1, 3, 2])
fig.show()
```

# Next

- Try plotly in panel.
- Add initial and final tangent vectors.
- Add method to change length of initial and final vectors.

# OLD

```
git clone https://github.com/sophiamyang/hvplot_interactive

conda create --name hvplot_interactive -c conda-forge hvplot panel pandas jupyterlab jupyter-panel-proxy jupyter_bokeh

conda activate hvplot_interactive

jupyter serverextension enable panel.io.jupyter_server_extension

conda install -c plotly plotly=5.11.0
```