# Resources

[3 Ways to Build a Panel Visualization Dashboard](https://towardsdatascience.com/3-ways-to-build-a-panel-visualization-dashboard-6e14148f529d) &rarr; Use the `pn.bind` method.  
[The Easiest Way to Create an Interactive Dashboard in Python:
Turn Pandas pipelines into a dashboard using hvPlot .interactive](https://towardsdatascience.com/the-easiest-way-to-create-an-interactive-dashboard-in-python-77440f2511d1)

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

## Convert to python file

`interactive_cubic_Bezier_curve.py`: Convert code from jupyter notebook into a regular python file. Run using:  

    panel serve interactive_cubic_Bezier_curve.py
    
## Try running a hello-world example as standalone html file

Use [Awesome panel hello-world example](https://github.com/awesome-panel/examples/blob/main/src/hello-world/app.py) and follow [How to Deploy a Panel Visualization Dashboard to GitHub Pages: The fastest way to deploy Python data apps](https://towardsdatascience.com/how-to-deploy-a-panel-visualization-dashboard-to-github-pages-2f520fd8660)

    (try_panel)
    $ panel convert example_single_file_app/app.py --to pyodide-worker --out docs/example_single_file_app
    Successfully converted example_single_file_app/app.py to pyodide-worker target and wrote output to app.html.

Then open html file in a browser.
    
## Try running as standalone html file
