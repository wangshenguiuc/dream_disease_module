'''
Author Nate Russell
ntrusse2@illinois.edu

Launch Server from command line with

bokeh serve /path/to/this/script/Scatter_Bokeh.py

Then use Chrome or Firefox to view the local host server @

    http://localhost:5006/Scatter_Bokeh

For best results, make sure your browser allows hardware acceleration and WebGL is turned on.

'''
accelerator = True  # If True, turns on WebGL
import bokeh
from bokeh.io import gridplot, output_file, output_server, vform
from bokeh.models import HBox, VBox, VBoxForm, BoxSelectTool, LassoSelectTool, Paragraph, HoverTool, WheelZoomTool, \
    PanTool, ResizeTool, SaveTool, RedoTool
from bokeh.models.layouts import WidgetBox
from bokeh.plotting import figure, hplot, vplot, curdoc, ColumnDataSource, show
from bokeh.models.widgets import TextInput, Button, DataTable, TableColumn
from matplotlib.cm import get_cmap
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams['legend.markerscale'] = 2
from matplotlib import gridspec
from matplotlib.colors import rgb2hex
import seaborn as sns

sns.set_context("paper", rc={"lines.linewidth": 0.9, "s": 0.05}, font_scale=1)
sns.set_style("white")
sns.set_style({'axes.facecolor': 'none'})
import random
import pandas as pd
import matplotlib.cm as cm
from bokeh.models.widgets import Slider, Select, TextInput
from sklearn.datasets import make_swiss_roll
from sklearn.cluster import KMeans
import warnings
from collections import defaultdict

def_quant_cmap = cm.get_cmap('viridis')
def_qual_cmap = cm.get_cmap('Paired')


def qual_2_color(X, dim_1=None, dim_2=None, cmap=def_qual_cmap):
    """

    :param X:
    :param dim_1:
    :param dim_2:
    :param cmap:
    :return:
    """
    if isinstance(X, np.ndarray):
        X = X.tolist()
    r = lambda: random.randint(0, 255)
    label = np.unique(X)
    #colors = ['#%02X%02X%02X' % (r(), r(), r()) for i in label]
    colors = [rgb2hex(cmap(float(i) / len(np.unique(label)))) for i in range(len(np.unique(label)))]

    mapper = dict(zip(label, colors))

    color_list = np.array([mapper.get(i) for i in X])

    return color_list


def rgb2hex(rgb):
    return '#%02x%02x%02x' % rgb[0:3]

def quant_2_color(x, n_colors=5, cmap=def_quant_cmap, robust='none', limit=3):
    """

    :param x:
    :param n_colors:
    :param cmap:
    :param robust:
    :param limit:
    :return:
    """
    if isinstance(x, np.ndarray):
        x = x.tolist()

    unique = np.unique(x)

    if len(unique) == 2:
        return ['#CC3300' if xi == unique[0] else '#0066CC' for xi in x]
    else:
        if robust == 'percentile':
            norm = mpl.colors.Normalize(vmin=np.percentile(x, 2), vmax=np.percentile(x, 98))
        elif robust == 'std':
            stdv = np.std(x)
            mu = np.mean(x)
            norm = mpl.colors.Normalize(vmin=max([min(x), (mu - (limit * stdv))]),
                                        vmax=min([max(x), (mu + (limit * stdv))]))
        else:
            norm = mpl.colors.Normalize(vmin=min(x), vmax=max(x))

        mapper = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
        rgba = mapper.to_rgba(x)
        rgba = rgba[:, 0:3]
        c = np.floor(rgba * 255)

        color_list = ['#%02X%02X%02X' % (c[i, 0], c[i, 1], c[i, 2]) for i in range(len(x))]

        return color_list


def is_numeric(obj):
    attrs = ['__add__', '__sub__', '__mul__', '__div__', '__pow__']
    return all(hasattr(obj, attr) for attr in attrs)


def get_color_map(c):
    """

    :param x:
    :return:
    """

    if isinstance(c[0], str) == False:
        color_list = quant_2_color(c, cmap=def_quant_cmap)
    else:
        color_list = qual_2_color(c, cmap=def_qual_cmap)

    return color_list


def make_plot(title, x, y):
    p = figure(tools=[HoverTool(tooltips=tooltip_list), LassoSelectTool(), WheelZoomTool(), PanTool(),SaveTool(),RedoTool(), ResizeTool(),
                      BoxSelectTool()], plot_width=600, plot_height=600, title=title, webgl=accelerator)
    p.xaxis.axis_label = "X Dimension"
    p.yaxis.axis_label = "Y Dimension"
    c = p.circle(x=x, y=y, size=8, color="__COLOR__", alpha=.75, source=source)
    p.select(BoxSelectTool).select_every_mousemove = False
    p.select(LassoSelectTool).select_every_mousemove = False

    return p, c


output_file('Scatter-Bokeh')

'''
----------------------------------------------------------------------------
Start Modification Region
----------------------------------------------------------------------------
'''
import sys
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)

num_embedding_files = int(sys.argv[1])
embedding_files = sys.argv[2].split(' ')
#meta_data_files = sys.argv[3]


maps_dict = {}
frames_list = []

print('Loading Data')
for f in embedding_files:


    print('Reading File: ' + f)
    # Extract File Names
    file_name = f.split('/')[-1]
    file_name = file_name.split('.')[0]

    # Read files
    tmp_df = pd.read_csv(f,nrows=70000)

    print('Columns:',tmp_df.columns)

    # Confirm it has X and Y columns
    try:
        tmp_x = tmp_df['V1']
        tmp_y = tmp_df['V2']
        tmp_df.drop(['V1', 'V2'], axis=1, inplace=True)
        tmp_df[file_name + ' V1'] = tmp_x
        tmp_df[file_name + ' V2'] = tmp_y
        maps_dict[file_name] = (file_name + ' V1', file_name + ' V2')

    except KeyError:
        raise KeyError('All Embedding Files must have an X and Y columns. Capitalization matters')

    # Add DF to master source
    frames_list.append(tmp_df)

# Concat Dataframes into one master source

df = pd.concat(frames_list, axis=1)
print(df.shape)
print(df.columns.values)


print("Success Here")

# Read MetaData File

#meta_df = pd.read_csv(meta_data_files)
#print(meta_df)
#df = pd.concat([df,meta_df],axis=1)
#print(df)







'''
----------------------------------------------------------------------------
End Modification Region
----------------------------------------------------------------------------
'''

# df = pd.read_csv('/home/nathan/Ubuntu/tsne_glove.csv')
n, p = df.shape
df["__COLOR__"] = ["#339933"] * n
df["__selected__"] = np.ones_like(n, dtype=np.bool)

df = df.to_dict(orient='list')

# Build Color Scheme
print("Building Color Dict and Color Select Tool...")
color_map_dict = {col: get_color_map(df[col]) for col in df.keys()}
color_selection = Select(title="Color By", options=df.keys(), value=df.keys()[0])

# Other Functionality
print("Initializing Buttons and Text input...")
selection_label = TextInput(value="MyGroup#1", title="Selection Label:")
save_selection = Button(label="Save Selection",)
add_selection_label = Button(label="Add Selection Label")
write_mod_file = Button(label="Write Modified File")


def save_selection_handler():
    print('APPLE')


def add_selection_handler():
    print('APPLE')


def write_selection_handler():
    print('APPLE')


save_selection.on_click(save_selection_handler)
add_selection_label.on_click(add_selection_handler)
write_mod_file.on_click(write_selection_handler)

# Build Tooltip
tooltip_list = [(col, "@" + col) for col in df.keys()]
tooltip_list = [('Token', "@Token")]

# Initialize HoverData
source = ColumnDataSource(data=df)
table_source = ColumnDataSource(data=df)


def update(attrname, old, new):
    print("\n------Update-----")

    # Get Original
    sdict = df

    # Update Color
    sdict["__COLOR__"] = color_map_dict[color_selection.value]
    print(color_selection.value)

    # Update Selected
    try:
        inds = np.array(new['1d']['indices'])
        num_pts = len(sdict["__COLOR__"])

        if len(inds) == 0 or len(inds) == num_pts:
            print("NOTHING SELECTED")
            pass
        else:
            x = np.arange(num_pts)
            print('Selected Set Size: ' + str(len(inds)))
            inds_bool = np.ones_like(x, dtype=np.bool)
            inds_bool[inds] = False
            print("Selected Index(s):")
            print(inds)
            print("Index Boolean")
            print(inds_bool)
            sdict["__selected__"] = inds_bool

            full_table_dict = df
            mod_table_dict = {col: np.array(full_table_dict[col])[inds] for col in full_table_dict.keys()}

            table_source.data = mod_table_dict

    # Hack to stop string index type error that occurs when you change color
    except TypeError:
        pass

    # Set New
    source.data = sdict


nested_grid_list = []
flat_list = []
exclude_from_table = ['__COLOR__']

for f in maps_dict.keys():
    xs = maps_dict[f][0]
    ys = maps_dict[f][1]
    p, c = make_plot(f, xs, ys)
    nested_grid_list.append(p)
    flat_list.append(c)
    exclude_from_table.append(xs)
    exclude_from_table.append(ys)

# Controls
controls = [color_selection, selection_label, save_selection, add_selection_label, write_mod_file]
for control in controls:
    control.on_change('value', update)

widgets = WidgetBox(children=controls)

# Add Table
data_table_columns = [col for col in df.keys() if col not in exclude_from_table]
columns = [TableColumn(field=col, title=col) for col in data_table_columns]
dt = DataTable(source=table_source, columns=columns, width=1800, height=230, scroll_to_selection=False,)

# data_table = DataTable(source=source, columns=columns, width=400, height=280)

# Grid Plot
nested_grid_list = list([nested_grid_list])
g = gridplot(nested_grid_list)


# Update Logic
for c in flat_list:
    c.data_source.on_change('selected', update)
curdoc().add_root(VBox(g,HBox(children=[widgets, WidgetBox(dt)], width=1800)))
