import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['legend.markerscale'] = 2
from matplotlib import gridspec
import seaborn as sns
sns.set_context("paper",rc={"lines.linewidth": 0.9,"s":0.05},font_scale=1)
sns.set_style("white")
sns.set_style({'axes.facecolor': 'none'})
import random
import matplotlib.cm as cm
from matplotlib.collections import LineCollection
from sklearn.datasets import  make_swiss_roll
from sklearn.cluster import KMeans
import warnings
from collections import defaultdict
from matplotlib.colors import rgb2hex
def_cmap = cm.get_cmap('Set1')


def is_numeric(obj):
    """
    Python 2 only!
    :param obj:
    :return:
    """
    attrs = ['__add__', '__sub__', '__mul__', '__div__', '__pow__']
    return all(hasattr(obj, attr) for attr in attrs)

def is_numeric(obj):
    attrs = ['__add__', '__sub__', '__mul__', '__truediv__', '__pow__']
    return all(hasattr(obj, attr) for attr in attrs)

def scatter_plot(X,c,c_type='auto',display=True,save_path=None,pt_size=44,contour=False,c_kde=True,
                 axis_label=None,title=None,verbose=False,colormap=def_cmap,alpha=0.7,G=None):
    """
    Wrapper function to help make static 2d and 3d scatter plots with colored points


    :param X: data you want to plot ,nx2 or nx3 numpy array of numerics
    :param c: quantitative or qualitative information you want to color by
    :param c_type: choices are 'auto', 'qual' or 'quant'. The latter two explicityly tell the function how to treat c
                   but 'auto' will assign 'qual' if c is an iterable of strings and 'quant' if c is an iterable of numerics
    :param display: if true, it will display to screen
    :param save_path: if a valid path, image will be saved
    :param pt_size: the size of the points plotted
    :param contour: traces grey gaussian KDE over 2d plots to see density of points
    :param c_kde: provides kde to show distribution or color for plots / always on for qualitative plots
    :param axis_label: list of strings for axis labels
    :param title: string for label of plot
    :param verbose: Not Implemented
    :param colormap: matplotlib colormap used in picking colors http://matplotlib.org/examples/color/colormaps_reference.html
    :param alpha: transparency
    :return: matplotlib.pyplot.figure object
    """

    # Check Input
    if not isinstance(X,np.ndarray):
        raise TypeError("X must be Numpy array of size nx2 or nx3")


    if c_type == 'auto':
        if is_numeric(c):
            color_list = quant_2_color(c,cmap=colormap)
            c_type = 'quant'
        else:
            color_list = qual_2_color(c,cmap=colormap)
            c_type = 'qual'
    elif c_type == 'quant':
        color_list = quant_2_color(c,cmap=colormap)
    elif c_type == 'qual':
        color_list = qual_2_color(c,cmap=colormap)
    else:
        warnings.warn("No valid c_type submitted...defaulting to automatic")


    if c_type == "qual":
        c_qual_count = defaultdict(float)
        for element in c:
            c_qual_count[element] += 1/len(c)

        c_qual_sizes = []
        unique_labels = np.unique(c)
        for label in unique_labels:
            c_qual_sizes.append(c_qual_count[label])
        sorted_labels = unique_labels[np.argsort(c_qual_sizes)][::-1]


    n,d = X.shape

    # 2d scatter plot
    if d == 2:

        fig = plt.figure(figsize=(6,6))
        gs = gridspec.GridSpec(2, 1, height_ratios=[15, 1])
        ax0 = plt.subplot(gs[0])

        # Add Edges
        if G != None:
            set_i,set_j = G.nonzero()
            set_w = G.data
            edges = LineCollection([[[X[i,0],X[i,1]],
                                     [X[j,0],X[j,1]]] for i,j in zip(set_i,set_j)],
                                   linestyles='solid',
                                   linewidths=(1),
                                   #colors=[(1,0,0) for i in set_i]
                                   )
            edges.set_array(set_w)
            ax0.add_collection(edges)
            axcb = fig.colorbar(edges)


        if c_type == "qual":
            if isinstance(c,list):
                c = np.array(c)



            for label,color in zip(sorted_labels,np.unique(color_list)):
                ax0.scatter(x = X[:,0][c == label],
                            y = X[:,1][c == label],
                            s = pt_size, c = color, label = str(label)+": ("+"{0:.2f}".format(c_qual_count[label])+")",
                            edgecolors='none',alpha=alpha,zorder=10)
        if c_type == "quant":
            ax0.scatter(x = X[:,0],y = X[:,1],s = pt_size, c = color_list,edgecolors='none',alpha=alpha)


        if contour:
            sns.kdeplot(X[:,0],X[:,1],cmap='Greys')


        plt.title(title)
        plt.xlabel(axis_label[0])
        plt.ylabel(axis_label[1])
        plt.margins(0.05)
        sns.despine(fig,top=True,left=False,right=True,bottom=False)


        # Configure Legend
        if c_type == "qual":
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
                      ncol=6, fancybox=True, shadow=True)
        if c_type == "quant":
            ax1 = fig.add_axes([0.12, 0.05, 0.8, 0.025])
            norm = mpl.colors.Normalize(vmin=min(c), vmax=max(c))
            cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=colormap,
                                norm=norm,
                                orientation='horizontal')

            if c_kde:
                ax2 = fig.add_axes([0.12, 0.1, 0.8, 0.05])
                sns.distplot(ax=ax2,a=c,hist=False,kde=True,rug=True,color='grey',kde_kws={'shade':True})
                ax2.set_xlim((min(c),max(c)))
                sns.despine(ax=ax2)
                ax2.axes.get_xaxis().set_visible(False)



        if isinstance(save_path,str):
            plt.savefig(save_path)

        if display:
            plt.show()


    elif d == 3:
        fig = plt.figure(figsize=(6,6))
        ax = fig.add_subplot(111, projection='3d')
        ax.set_title(title)

        if c_type == 'quant':
            ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=color_list,edgecolors='none',s=pt_size,alpha=alpha)
        elif c_type == 'qual':

            # must convert to array to use the logical indexing [c == label]
            if isinstance(c,list):
                c = np.array(c)

            for label,color in zip(sorted_labels,color_list):
                ax.scatter(X[:,0][c == label],
                           X[:,1][c == label],
                           X[:,2][c == label],
                           c=color,
                           edgecolors='none',s=pt_size,
                           alpha=alpha,label=str(label)+": ("+"{0:.2f}".format(c_qual_count[label])+")")


        # White opaque back panels
        ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
        ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))
        ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 1.0))

        if isinstance(axis_label,list):
            plt.xlabel(axis_label[0])
            plt.ylabel(axis_label[1])
            ax.set_zlabel(axis_label[2])

        # Configure Legend
        if c_type == "qual":
            ax.legend(loc='upper center', bbox_to_anchor=(0.5, 0),
                      ncol=6, fancybox=True, shadow=True)
        if c_type == "quant":
            ax1 = fig.add_axes([0.12, 0.05, 0.8, 0.025])
            norm = mpl.colors.Normalize(vmin=min(c), vmax=max(c))
            cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=colormap,
                                norm=norm,
                                orientation='horizontal')
            if c_kde:
                ax2 = fig.add_axes([0.12, 0.1, 0.8, 0.05])
                sns.distplot(ax=ax2, a=c, hist=False, kde=True, rug=True, color='grey', kde_kws={'shade': True})
                ax2.set_xlim((min(c), max(c)))
                sns.despine(ax=ax2)
                ax2.axes.get_xaxis().set_visible(False)

        if display:
            plt.show()
    else:
        raise ValueError('X must by n x 2 or n x 3, instead you passed '+str(X.shape))

def qual_2_color(X, dim_1=None, dim_2=None,cmap=def_cmap):
    """

    :param X:
    :param dim_1:
    :param dim_2:
    :param cmap:
    :return:
    """
    if isinstance(X,np.ndarray):
        X = X.tolist()
    r = lambda: random.randint(0, 255)
    label = np.unique(X)
    #colors = ['#%02X%02X%02X' % (r(), r(), r()) for i in label]


    colors = [rgb2hex(cmap(float(i) / len(label))) for i in range(len(label))]


    mapper = dict(zip(label, colors))
    color_list = np.array([mapper.get(i) for i in X])

    return color_list




def quant_2_color(x, n_colors=5, cmap=None, robust='none', limit=3):
    """

    :param x:
    :param n_colors:
    :param cmap:
    :param robust:
    :param limit:
    :return:
    """
    if isinstance(x,np.ndarray):
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

def demo_functionality():
    """
    Hard Coded example usages of this script
    :return: None
    """
    print("Testing Swiss Roll Variations")
    n = 1000
    x_test,t = make_swiss_roll(n,random_state=1234,noise=1)
    categorical = ["Class_"+str(label) for label in KMeans(n_clusters=50).fit_predict(x_test)]
    x_test_2d = np.vstack((x_test[:,0],x_test[:,2])).T

    fig1 = scatter_plot(X=x_test_2d,c=t,c_type='auto',axis_label=['x1','x2','x3'])
    fig2 = scatter_plot(X=x_test_2d,c=categorical,c_type='qual',axis_label=['x1','x2','x3'])
    fig3 = scatter_plot(X=x_test,c=t,c_type='auto',axis_label=['x1','x2','x3'],title='3D Quant',colormap=cm.get_cmap('Spectral'))
    fig4 = scatter_plot(X=x_test,c=categorical,c_type='auto',axis_label=['x1','x2','x3'],title='3D Qual',colormap=cm.get_cmap('Set1'))


def graph_plot():
    """

    :return:
    """
    return


if __name__ == "__main__":
    demo_functionality()
