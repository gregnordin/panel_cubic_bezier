# Resources

- [3 Ways to Build a Panel Visualization Dashboard](https://towardsdatascience.com/3-ways-to-build-a-panel-visualization-dashboard-6e14148f529d) &rarr; Use the `pn.bind` method.  
- [The Easiest Way to Create an Interactive Dashboard in Python:
Turn Pandas pipelines into a dashboard using hvPlot .interactive](https://towardsdatascience.com/the-easiest-way-to-create-an-interactive-dashboard-in-python-77440f2511d1).
- [Panel Docs: Running Panel in the Browser with WASM](https://panel.holoviz.org/user_guide/Running_in_Webassembly.html).

# Install conda environment

See 2nd link in Resources.

```
conda create -n "try_panel" python=3.10
conda activate try_panel 
conda install hvplot panel pandas jupyterlab black
```

# Saturday, 11/5/22

[Start panel notebook from command line](https://panel.holoviz.org/user_guide/Overview.html#command-line):

    panel serve 2022-11-03_interactive_cubic_bezier.ipynb

[How to Deploy a Panel Visualization Dashboard to GitHub Pages](https://towardsdatascience.com/how-to-deploy-a-panel-visualization-dashboard-to-github-pages-2f520fd8660)

    panel convert 2022-11-03_interactive_cubic_bezier.ipynb --to pyodide-worker --out docs/app

# Monday, 11/7/22

## Put unit circle on visualization

Use `hv.Polygons` to create a unit circle to visually denote start and end point for interactive cubic Bezier curve.

## Convert to python file and run with `panel serve`

`interactive_cubic_Bezier_curve.py`: Convert code from jupyter notebook into a regular python file. Run using:  

    panel serve interactive_cubic_Bezier_curve.py
    
## Try running a hello-world example as standalone html file

Use [Awesome panel hello-world example](https://github.com/awesome-panel/examples/blob/main/src/hello-world/app.py) and follow [How to Deploy a Panel Visualization Dashboard to GitHub Pages: The fastest way to deploy Python data apps](https://towardsdatascience.com/how-to-deploy-a-panel-visualization-dashboard-to-github-pages-2f520fd8660)

    (try_panel)
    $ panel convert example_single_file_app/app.py --to pyodide-worker --out docs/example_single_file_app
    Successfully converted example_single_file_app/app.py to pyodide-worker target and wrote output to app.html.

Then open html file in a browser.
    
## Try running interactive Bezier curve as standalone html file

```
(try_panel)
$ panel convert interactive_cubic_Bezier_curve.py --to pyodide-worker --out docs/interactive_cubic_Bezier_curve
Successfully converted interactive_cubic_Bezier_curve.py to pyodide-worker target and wrote output to interactive_cubic_Bezier_curve.html.
```

To run, start http server:

```
(try_panel)
nordin@ECEns-MBP-4 ~/Documents/Projects/2022_Projects/panel_cubic_bezier (main)*
$ python -m http.server
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

and point browser at `http://localhost:8000/docs/interactive_cubic_Bezier_curve/interactive_cubic_Bezier_curve.html`. Tried `Brave`, `Safari`, `Chrome`.

**Problems**

- Slider control points are not visible, making it very inconvenient to change values.
- Theme toggle does not work.
- Sidebar toggle does not work.

## As a PWA

```
(try_panel)
$ panel convert interactive_cubic_Bezier_curve.py --to pyodide-worker --pwa --title "Interactive Cubic Bezier Curve" --out docs/interactive_cubic_Bezier_curve_pwa
Successfully converted interactive_cubic_Bezier_curve.py to pyodide-worker target and wrote output to interactive_cubic_Bezier_curve.html.
Successfully wrote icons and images.
Successfully wrote site.manifest.
Successfully wrote serviceWorker.js.
```

To run, start http server:

```
(try_panel)
nordin@ECEns-MBP-4 ~/Documents/Projects/2022_Projects/panel_cubic_bezier (main)*
$ python -m http.server
Serving HTTP on :: port 8000 (http://[::]:8000/) ...
```

and point browser at `http://localhost:8000/docs/interactive_cubic_Bezier_curve_pwa/interactive_cubic_Bezier_curve.html`. It loads faster than the non-pwa version.

## Serve with Github Pages

Follow [How to Deploy a Panel Visualization Dashboard to GitHub Pages: The fastest way to deploy Python data apps](https://towardsdatascience.com/how-to-deploy-a-panel-visualization-dashboard-to-github-pages-2f520fd8660) to serve `docs/` and with browser go to:

    https://gregnordin.github.io/panel_cubic_bezier/interactive_cubic_Bezier_curve/interactive_cubic_Bezier_curve.html

**It works**, subject to the problems noted above.

Note: I changed the repository from private to public so anyone can see it.


# Tuesday, 11/8/22

## Improve performance

Based on Philipp Rudiger's suggestion at [Github Pages-widget rendering problems](https://discourse.holoviz.org/t/github-pages-widget-rendering-problems/4524), replace

```
interactive_bezier = pn.bind(
    bezier_curve_bind,
    p1_angle_deg_slider,
    d0_length_slider,
    d0_angle_deg_slider,
    d1_length_slider,
    d1_angle_deg_slider,
)
```

with 

```
interactive_bezier = hv.DynamicMap(
    bezier_curve_bind, streams={
        'p1_angle_deg': p1_angle_deg_slider,
        'd0_length': d0_length_slider,
        'd0_angle_deg': d0_angle_deg_slider,
        'd1_length': d1_length_slider,
        'd1_angle_deg': d1_angle_deg_slider,
    }
)
```

> ...note that you can get a much more performant app.... This ensure that HoloViews updates the individual components rather than redrawing the entire plot.


# Next

- &#9989; Fix problems above.
    - &#10060; Try a different template.
    - &#9989; Post problems on Holoviz Discourse.
        - [Github Pages-widget rendering problems](https://discourse.holoviz.org/t/github-pages-widget-rendering-problems/4524)
- Add explanatory text to app webpage.
- Improve start and end point section visual presentation.
- Put start and endpoint arrays and tangent arrays in text area that can be copied as python code?


# Wednesday, 11/9/22

## Play with plotly `line_3D`

- Use `marker` to make line appear thick in 3D. Setting `line` `width` doesn't give a satisfactory result.
- Remove background x-y-z panels so it is easier to get a sense of 3 dimensions for a plotted line.


# Thursday, 11/10/22

## Begin to work on sequential cubic Bezier curves

### Explore using in and out tangents for each point in curve

`n_points = n_Bezier_segments + 1`

`2022-11-10_sequential_cubic_beziers.ipynb` &rarr; didn't work.

`link_tabulator_plot.py`

- Successfully change Tabulator values, which updates a dataframe, which updates a df.hvplot() line plot.
- Key resource: [Linking Tabulator with a HV plot](https://discourse.holoviz.org/t/linking-tabulator-with-a-hv-plot/2377/2).

## Next

- &#9989; Replace tabulator with one for points and tangents.
- &#9989; Replace dataframe calculated from tabular with one that has sequential cubic Bezier curves.
- &#9989; Line plot of sequential cubic Bezier curves.
- &#9989; Add scatter plot of points ~~with `name` as P0, P1, P2, etc.~~


# Friday, 11/11/22

## Continue working on sequential cubic Bezier curves

`panel_tabulator/2_tabulator_cubic_Bezier_params.py`

- Link tabulator and scatter plot of points.
- Include table of absolute positions and change scatter plot to visualize.
- Successfully make interactive sequential Bezier curve with 2 segments.
- Increase to 3 segments.

## Next

- Automate for variable number of segments.
- &#9989; Pad the x and y limits of plot (or fix the limits).
- Better colors.
- Make colors cyclic.
- Add switch to change colors between cyclic and the same.


