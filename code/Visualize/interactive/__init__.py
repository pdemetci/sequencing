import numpy as np
import bokeh
import bokeh.io
import bokeh.plotting
import pandas as pd
import matplotlib.colors
import matplotlib.cm
import os.path
import glob
import IPython.display
from collections import defaultdict
from external_coffeescript import build_callback
import meta
import argparse

bokeh.io.output_notebook()

def build_selected(indices):
    pvd = bokeh.core.property.containers.PropertyValueDict
    pvl = bokeh.core.property.containers.PropertyValueList

    selected = pvd({
        '0d': pvd({
            'glyph': None,
            'indices': pvl(),
        }),
        '1d': pvd({
            'indices': pvl(indices),
        }),
        '2d': pvd(),
    })

    return selected
from bokeh.plotting import figure, output_file, show
from bokeh.charts import Scatter, output_file, show
import pandas as pd
import csv
import numpy as np
from bokeh.models import HoverTool, ColumnDataSource
from collections import OrderedDict
from bokeh.layouts import row, column
from bokeh.models import BoxSelectTool, LassoSelectTool, Spacer
from bokeh.plotting import figure, curdoc, show

def scatter(filename= 'sample.csv', x_column='Condition 1', y_column='Condition 2', title='Title', x_label='x-label', y_label='y-label', log_scale=True, histogram=False,
    num_bins=5, color_column='Type', colormap={'Type A Gene': 'red', 'Type B Gene':'green','Type C Gene':'blue'}):

    df= pd.DataFrame.from_csv(filename)
    output_file('index.html')

    TOOLS="resize, save, pan, box_zoom,reset,tap, box_select, lasso_select"
    source=ColumnDataSource(data=dict(
        label=df["Gene"].tolist(),
        desc=df['Description'].tolist(),
        type=df['Type'].tolist()
        ))
    # output to static HTML file
    hover=HoverTool(tooltips=[
        ("label", "@label"),
        ("(x,y)", "(@x, @y)"),
        ("desc", "@desc"),
        ("type", "@type")
        ])
    colormap={'Type A Gene': 'red', 'Type B Gene':'green','Type C Gene':'blue'}
    colors=[colormap[x] for x in df[color_column]]
    if log_scale==True:
        p = figure(plot_width=600, plot_height=600, title=title, x_axis_label=x_label, y_axis_label=y_label, x_axis_type='log', y_axis_type='log', tools=[hover, TOOLS])
        p.title.text_font_size='20pt'
    
    else:
        p = figure(plot_width=600, plot_height=600, title=title, x_axis_label=x_label, y_axis_label=y_label, tools=[hover, TOOLS])
        p.title.text_font_size='20pt'
    p.scatter(df[x_column], df[y_column], size=20, color=colors, source=source)
    if histogram==True:
        #create horizontal histogram
        x=df[x_column]
        y=df[y_column]
        hhist, hedges = np.histogram(x, bins=num_bins)
        hzeros = np.zeros(len(hedges)-1)
        hmax = max(hhist)*1.1

        LINE_ARGS = dict(color="#3A5785", line_color=None)

        ph = figure(toolbar_location=None, plot_width=p.plot_width, plot_height=200, x_range=p.x_range,
                    y_range=(-hmax, hmax), min_border=10, min_border_left=50, y_axis_location="right")
        ph.xgrid.grid_line_color = None
        ph.yaxis.major_label_orientation = np.pi/4
        # ph.background_fill_color = "#fafafa"

        ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hhist, color="white", line_color="#3A5785")
        hh1 = ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.5, **LINE_ARGS)
        hh2 = ph.quad(bottom=0, left=hedges[:-1], right=hedges[1:], top=hzeros, alpha=0.1, **LINE_ARGS)

        # create the vertical histogram
        vhist, vedges = np.histogram(y, bins=num_bins)
        vzeros = np.zeros(len(vedges)-1)
        vmax = max(vhist)*1.1

        pv = figure(toolbar_location=None, plot_width=200, plot_height=p.plot_height, x_range=(-vmax, vmax),
                    y_range=p.y_range, min_border=10, y_axis_location="right")
        pv.ygrid.grid_line_color = None
        pv.xaxis.major_label_orientation = np.pi/4
        # pv.background_fill_color = "#fafafa"

        pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vhist, color="white", line_color="#3A5785")
        vh1 = pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vzeros, alpha=0.5, **LINE_ARGS)
        vh2 = pv.quad(left=0, bottom=vedges[:-1], top=vedges[1:], right=vzeros, alpha=0.1, **LINE_ARGS)

        layout = column(row(p, pv), row(ph, Spacer(width=200, height=200)))


        show(layout)
    else:
        show(p)
scatter(filename='sample.csv', x_column='Condition 1', y_column='Condition 2', x_label='x-label', y_label='y-label', log_scale=False, histogram=True, num_bins=5, color_column='Type', colormap={'Type A Gene': 'red', 'Type B Gene':'green','Type C Gene':'blue'})
