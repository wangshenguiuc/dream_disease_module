from sklearn import datasets
from sklearn.decomposition import TruncatedSVD
from sklearn.manifold import TSNE
from scipy.sparse import csr_matrix, dok_matrix
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
from scipy.spatial.distance import euclidean
import subprocess
import os
import tempfile
import pandas as pd
from plotting_util import scatter_plot
from sklearn.neighbors import NearestNeighbors
from largevis import LargeVis
from collections import defaultdict



def read_csrmat_file(path):
    """

    :param path:
    :return:
    """

    return 1

class Graph:

    def __init__(self,x=None,i=None,j=None,w=None,path=None,filetype='edgelist',directed=False,verbose=True):
        """

        :param x:
        :param i:
        :param j:
        :param w:
        :param directed:
        :param verbose:
        """
        self.verbose = verbose
        self.edgelist_path = 'None'
        self.directed = directed
        if self.verbose: print("Initializing Graph Instance...")

        # initialize graph object depending on data format
        # sparse matrix format
        if isinstance(x,sp.sparse.csr.csr_matrix):
            if self.verbose: print('CSR_Matrix Detected')
            self.G = x

        # dense matrix
        elif isinstance(x,np.matrixlib.defmatrix.matrix):
            if self.verbose: print('Numpy Matrix Detected')
            self.G = csr_matrix(x)

        # edge list format
        elif hasattr(i, '__iter__') and hasattr(i, '__iter__') and hasattr(i, '__iter__'):
            if self.verbose: print('Iterable Edge list format detected')
            if len(i) == len(j) == len(w):
                if self.verbose: print('i,j,w are all same length, hooray')
                self.G = csr_matrix(w,(i,j))
            else:
                ValueError('i,j,w must all be same length')

        # existing file
        elif os.path.exists(path):
            if verbose: print("File on disk Detected")
            if filetype == 'edgelist':
                self.G = self.read_edgelist_file(path)
                if verbose: print("G successfully set")
            elif filetype == 'csrmat':
                self.G = read_csrmat_file(path)
            else:
                ValueError('file type not recognize')

        else:
            ValueError('Initialization data was not valid')

    def read_edgelist_file(self,path):
        """
        converts edge list format text file to csr matrix

        :param path:
        :return:
        """

        i_list = []
        j_list = []
        w_list = []
        node_ids = []
        id_2_int_dict = defaultdict(int)
        int_2_id_dict = defaultdict(str)

        tmpdir = tempfile.mkdtemp()
        tmpfile = tmpdir + "/edge_list_file.txt"

        if os.path.exists(path):

            with open(path, mode='r') as f:
                for line in f:
                    i, j, _ = line.split()
                    node_ids.append(i)
                    node_ids.append(j)
            unique_node_ids = np.unique(node_ids)
            for i,id in enumerate(unique_node_ids):
                id_2_int_dict[id] = i
                int_2_id_dict[i] = id

            with open(path, mode='r') as f:
                with open(tmpfile, mode='w') as tmp:
                    for line in f:
                        i, j, w = line.split()
                        i = id_2_int_dict[i]
                        j = id_2_int_dict[j]

                        i_list.append(i)
                        j_list.append(j)
                        w_list.append(float(w))

                        # writing data to disk
                        tmp.write(str(i) + ' ' + str(j) + ' ' + str(w) + '\n')
                        if self.directed == False:
                            tmp.write(str(j) + ' ' + str(i) + ' ' + str(w) + '\n')

            self.edgelist_path = tmpfile



        else:
            raise ValueError('No file detected: ' + path)

        data = (w_list, (i_list, j_list))

        self.id_2_int = id_2_int_dict
        self.int_2_id = int_2_id_dict

        return csr_matrix(data)

    def get_edgelist_file(self,symetric=True,storage_path=None):
        """
        Checks if edgelist format already exists on disk, if it does, return the path
        if one does not already exist, it will create one in a temp folder
        :return:
        """
        if self.directed == True:
            symetric = False

        if os.path.exists(self.edgelist_path):
            return self.edgelist_path
        else:
            # make named temp file
            if storage_path == None:
                tmpdir = tempfile.mkdtemp()
                tmpfile = tmpdir+"/edge_list_file.txt"
            else:
                tmpfile = storage_path

            with open(tmpfile,mode='w') as f:

                # assuming i,j,w are available
                try:
                    for i,j,w in zip(self.i,self.j,self.w):
                        f.write(str(i) + ' ' + str(j) + ' ' + str(w) + '\n')
                        if symetric:
                            f.write(str(j) + ' ' + str(i) + ' ' + str(w) + '\n')
                except AttributeError:

                    # Convert CSR format to ijw file
                    self.i, self.j = self.G.nonzero()
                    self.w = self.G.data


                    for i, j, w in zip(self.i, self.j, self.w):
                        if i != j:
                            f.write(str(i) + ' ' + str(j) + ' ' + str(w) + '\n')
                            if symetric:
                                f.write(str(j) + ' ' + str(i) + ' ' + str(w) + '\n')
                        else:
                            print("\nOh No! i == j")

            # Stash it and return
            self.edgelist_path = tmpfile
            return tmpfile



def save_sparse_csr(filename,array):
    np.savez(filename,data = array.data ,indices=array.indices,
             indptr =array.indptr, shape=array.shape )

def load_sparse_csr(filename):
    loader = np.load(filename)
    return csr_matrix((  loader['data'], loader['indices'], loader['indptr']),
                         shape = loader['shape'])

def csr_2_text(G):
    """

    :param G:
    :return:
    """


def matrix_2_sparse_graph(M, prob=0.5, knn=2):
    """
    Convert Vector representation of data into a sparsely sampled similarity graph
    :param M:
    :param p:
    :return:
    """

    n, p = M.shape
    print('Randomly Populating Affinity Matrix')

    if knn >= 1:
        print('Computing KNN graph')
        model = NearestNeighbors(n_neighbors=knn)
        model.fit(M)
        X = model.kneighbors_graph(n_neighbors=knn,mode='distance')
        X.data = -X.data + max(X.data)
        print('Done getting knn')
        print(type(X))
        print(X)
        return X
    else:
        X = csr_matrix((n, n), dtype=np.float64)
        print(type(X))
        dmax = 0
        for i in range(n):
            for j in range(i):
                rf = np.random.random()
                if rf < prob:
                    sim = 1 / euclidean(M[i, :], M[j, :])
                    X[i, j] = sim
                    X[j, i] = sim
                    dmax = max(dmax, sim)
        X += np.diag(np.ones(n)) * dmax

    return X


class tsvd_embed:
    """
    Simple Naive Baseline for embedding graph via Truncated SVD
    """

    def __init__(self, n_components):
        self.n_components = n_components
        self.model = TruncatedSVD(n_components=self.n_components)

    def fit(self, G):
        self.model.fit(G.G)

    def transform(self, G):
        return self.model.transform(G.G)

    def fit_transform(self, G):
        self.model.fit(G.G)
        return self.model.transform(G.G)


def embedding_2_X(path):
    """

    :param path:
    :return:
    """
    counter = -1
    with open(path, mode='r') as f:
        for line in f:

            if counter == -1:
                n, p = line.split()
                n, p = int(n), int(p)

                print('Output dimensions', n, p)
                X = np.ones((n, p))
                labels = np.ones(n)

            else:
                row_id = int(line.split()[0])
                X[row_id, 0:p] = np.array([float(x) for x in line.split()[1:p + 1]])

            counter += 1

    print("\nData Shape:" + str(X.shape))

    return X



class node2vec:
    def __init__(self,n_componenets=100,walk_length=10,num_walks=10,window_size=10,n_iter=1,workers=8,p=1,q=1,weighted=True,undirected=True):
        self.ncomps = n_componenets
        self.walklength = walk_length
        self.numwalks = num_walks
        self.windowsize = window_size
        self.iter = n_iter
        self.workers = workers
        self.p = p
        self.q = q
        self.weighted  = weighted
        self.undirected = undirected

        if self.weighted == True:
            self.weighted_string = '--weighted'
        else:
            self.weighted_string = '--unweighted'

        if self.undirected == True:
            self.directed_string = '--undirected'
        else:
            self.directed_string = '--directed'


    def fit_transform(self,G):
        """

        :param G:
        :return:
        """
        in_file = G.get_edgelist_file(symetric=False)
        tmpdir = tempfile.mkdtemp()
        out_file = tmpdir + '/outfile.txt'

        start_dir = os.curdir

        print("Starting Dir: " + start_dir)

        current_pardir = os.path.abspath(os.path.join(os.curdir, os.pardir))
        os.chdir(current_pardir + '/Network_Embedding_Methods/node2vec/')
        arg_list = ['python','src/main.py',
                    '--dimensions', str(self.ncomps),
                    '--output',out_file,
                    '--input',in_file,
                    '--walk-length', str(self.walklength),
                    '--num-walks', str(self.numwalks),
                    '--window-size', str(self.windowsize),
                    '--iter', str(self.iter),
                    '--workers', str(self.workers),
                    '--p', str(self.p),
                    '--q', str(self.q),
                    self.weighted_string,
                    self.directed_string,
                    ]
        print(' '.join(arg_list))
        subprocess.call(arg_list)
        # Change back to origanl dir
        os.chdir(current_pardir + '/Pipeline/')
        print("Ending Dir: " + os.curdir)

        # Read result back into memory
        print("\nReading LINE output vectors into Python Memory...")
        D = embedding_2_X(out_file)
        print("Done")

        return D

class LINE:
    def __init__(self,n_components=100,order=2,
                 neg=5,nthreads=8,nsamples=10,depth=2,kmax=500,threshold=5):
        self.n_components = n_components
        self.order = order
        self.neg = neg
        self.nthreads = nthreads
        self.nsamples = nsamples
        self.depth = depth
        self.kmax = kmax
        self.threshold = threshold


    def read_line_vector_file(self,path):
        """

        :param path:
        :return:
        """


        counter = -1
        with open(path, mode='r') as f:
            for line in f:

                if counter == -1:
                    n, p = line.split()
                    n, p = int(n), int(p)

                    print('Output dimensions',n,p)
                    X = np.ones((n, p))
                    labels = np.ones(n)

                else:
                    row_id = int(line.split()[0])
                    X[row_id, 0:p] = np.array([float(x) for x in line.split()[1:p + 1]])

                counter += 1

        print("\nData Shape:" + str(X.shape))

        return X

    def fit_transform(self,G):
        """

        :param G:
        :return:
        """

        in_file = G.get_edgelist_file()
        tmpdir = tempfile.mkdtemp()
        out_file = tmpdir+'/outfile.txt'

        start_dir = os.curdir

        print("Starting Dir: "+start_dir)

        current_pardir = os.path.abspath(os.path.join(os.curdir, os.pardir))
        os.chdir('/data/work/ntrusse2/dream_dmi_dev/Network_Embedding_Methods/LINE/linux/')
        print("Entering dir: "+os.curdir)
        print("In edgelist: "+in_file)
        arg_list = ['./run_line.sh',
                         '-d',str(self.n_components),
                         '-o', str(2),
                         '-i', str(in_file),
                         '-x', str(out_file),
                         '-t', str(self.nthreads),
                         '-n', str(self.neg),
                         '-s', str(self.nsamples),
                         '-k', str(self.kmax),
                         '-p', str(self.depth),
                         '-r',str(self.threshold),
                         ]
        print(' '.join(arg_list))
        # Change to dir and call bash with arg list
        os.chdir(current_pardir + '/Network_Embedding_Methods/LINE/linux/')
        subprocess.call(arg_list)
        # Change back to origanl dir
        os.chdir(current_pardir + '/Pipeline/')
        print("Ending Dir: " + os.curdir)

        # Read result back into memory
        print("\nReading LINE output vectors into Python Memory...")
        D = self.read_line_vector_file(out_file)
        print("Done")

        return D


def test_graph_embedding(viz=True):
    """

    :return:
    """
    # Generate datasets. We choose the size big enough to see the scalability
    # of the algorithms, but not too big to avoid too long running times
    n_samples = 2000
    percent_edge_sample = 1

    noisy_circles = datasets.make_circles(n_samples=n_samples, factor=.5, noise=0.05)
    noisy_moons = datasets.make_moons(n_samples=n_samples, noise=.05)
    blobs = datasets.make_blobs(n_samples=n_samples,centers=6,cluster_std=0.5, random_state=8)
    no_structure = np.random.rand(n_samples, 2), np.ones(n_samples)

    X, y = blobs
    print("Initializing Graph Object")
    Xtest = matrix_2_sparse_graph(X,knn=5,prob=0.1)
    Gtest = Graph(x=Xtest)

    if viz:
        print('First Viz')
        scatter_plot(X, ['Set_' + str(i) for i in y], axis_label=['X', 'Y'],display=False,
                     title='Original Space', alpha=1,G=Gtest.G,save_path='/data/work/ntrusse2/mypic.jpg')

    print(type(Gtest))

    #------------------------------------------------------------------------------------------------------------------
    print("Initalizing node2vec")
    model = node2vec(n_componenets=50,walk_length=10,num_walks=100,window_size=10,n_iter=10) # tsvd_embed(50)
    print("Testing Transform")
    V = model.fit_transform(Gtest)
    D = TruncatedSVD(n_components=2).fit_transform(V)
    if viz:
        scatter_plot(D, ['Set_' + str(i) for i in y], axis_label=['X', 'Y'], title='TSVD of node2vec', alpha=1, G=Gtest.G)
        lv = largevis(K=10, n_trees=5, max_iter=10, dim=2, M=5, gamma=7, alpha=1, rho=1)
        D = lv.fit_transform(V)
        scatter_plot(D, ['Set_' + str(i) for i in y], axis_label=['X', 'Y'], title='LargeVis of node2vec', alpha=1)

    print("Initalizing LINE")
    model = LINE(n_components=3,order=2,nsamples=100,kmax=1,depth=2,threshold=75)#tsvd_embed(50)
    print("Testing Transform")
    V = model.fit_transform(Gtest)


    D = TruncatedSVD(n_components=2).fit_transform(V)
    if viz:
        scatter_plot(D, ['Set_' + str(i) for i in y], axis_label=['X', 'Y'], title='TSVD of LINE',alpha=1,G=Gtest.G)
        lv = largevis(K=100, n_trees=5, max_iter=10, dim=2, M=5, gamma=7, alpha=1, rho=1)
        D = lv.fit_transform(V)
        scatter_plot(D, ['Set_' + str(i) for i in y], axis_label=['X', 'Y'], title='LargeVis of LINE', alpha=1)

    D = TruncatedSVD(n_components=2).fit_transform(Xtest)
    if viz:
        scatter_plot(D, ['Set_' + str(i) for i in y], axis_label=['X', 'Y'], title='TSVD Plain', alpha=1,G=Gtest.G)
        lv = largevis(K=100, n_trees=5, max_iter=10, dim=2, M=5, gamma=7, alpha=1, rho=1)
        D = lv.fit_transform(TruncatedSVD(n_components=100).fit_transform(Xtest))
        scatter_plot(D, ['Set_' + str(i) for i in y], axis_label=['X', 'Y'], title='LargeVis of LINE', alpha=1)



if __name__ == "__main__":
    test_graph_embedding()






