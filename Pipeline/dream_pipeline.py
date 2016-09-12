from Pipeline.Graph_Embed import *
import os
from sklearn.preprocessing import normalize
from sklearn.neighbors import NearestNeighbors


def load_networks(parent_dir):
    """
    Load networks from parent_directory

    :param parent_dir: parent dir where all network files reside inside
    :return: sorted list of absolute file path strings
    """

    print("Searching for Network Files...")

    file_list = []
    for file in os.listdir(parent_dir):
        if file.endswith(".txt"):
            if not file.startswith("README"):
                file_list.append(parent_dir+file)

    # sort the list so networks are in order, just an aesthetic thing
    file_list.sort()

    print("Found "+ str(len(file_list))+" Files: ")
    for f in file_list:
        print("\t"+f)

    return file_list

def embed_networks(network_files,out_dir):
    """
    Load network as graph object, then embed them and save the embeddings to the out-dir

    :param network_files: list of network files
    :param out_dir: location where embedding files are dumped
    :return: TRUE if completed succesfully
    """

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    models = {"LINE":LINE(n_components=100, order=2, nsamples=100, kmax=1, depth=2, threshold=50),
              "Node2Vec":node2vec(n_componenets=100)}

    for mkey in models:

        print("\n---"+mkey+"---")
        model = models[mkey]

        for f in network_files:
            print("\n-"+f)
            g = Graph(path=f)
            V = model.fit_transform(g)

            print(V)

def embedding_2_knn(X,k,metric='euclidean'):
    """
    build aproximate knn graph from vector space. Edges will be weighted via "flip & shift" to reflect similarity instead of distance

    :param X: n,p dense matrix
    :param k: # of neighbors
    :param metric: distance function between points in X
    :return: matrix
    """

    model = NearestNeighbors(n_neighbors=k)
    model.fit(X)
    X = model.kneighbors_graph(n_neighbors=k, mode='distance')
    X.data = -X.data + max(X.data)

    print(type(X))

    return X

def knn_2_edgelist(knn_mat,graph,out_path):
    """

    :param knn_mat: CSR Neighborhood graph
    :param out_path: location that edge list should be written too
    :return: True if completed succesfully
    """

    # Convert CSR format to ijw file
    ii, jj = knn_mat.nonzero()
    ww = knn_mat.data

    with open(out_path,mode='w') as f:
        for i, j, w in zip(ii, jj, ww):
            if i != j:

                if graph != None:
                    i = graph.int_2_id[i]
                    j = graph.int_2_id[j]

                f.write(str(i) + ' ' + str(j) + ' ' + str(w) + '\n')
                f.write(str(j) + ' ' + str(i) + ' ' + str(w) + '\n')
            else:
                'Huge Issue. knn shouldnt have itself as neighbor!'


    return True



