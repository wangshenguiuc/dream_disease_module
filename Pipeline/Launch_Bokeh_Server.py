import subprocess
import os
import webbrowser
import numpy as np
from largevis import LargeVis
from functools import reduce
import pandas as pd


def launch_localhost():
    """

    :return:
    """
    current_pardir = os.path.abspath(os.path.join(os.curdir, os.pardir))
    os.chdir(current_pardir + '/Pipeline')
    print("Launching WebBrowser...")
    webbrowser.open("http://localhost:5006/Scatter_Bokeh?webgl=1", new=1, autoraise=True)  # localhost:5006/Scatter_Bokeh
    print("Starting Server...")

    embedding_files = '/home/nathan/psb_largevis2.csv'
    meta_data_files = '/home/nathan/Downloads/dataset7_mod.csv'


    subprocess.call(["bokeh", "serve","Scatter_Bokeh.py","--args",embedding_files,'/home/nathan/psb_pca.csv',meta_data_files])


def intersect(*d):
    sets = iter(map(set, d))
    result = sets.next()
    for s in sets:
        result = result.intersection(s)
    return result



def launch_wordembedding_localhost(we_list,path='/home/nathan/'):
    """
    Given a list of word embedding objects, make sure they match eachother, and launch the vis using largevis


    :param we_list:
    :return:
    """

    print("\nStarting Word Viz")


    word_sets = []


    for we in we_list:

        print(we.name)
        X = we.X
        words = we.words

        word_sets.append(words)

        print("Word Embedding Space shape:")
        print(X.shape)
        print("# of Words: "+str(len(words)))


    print("\nComputing Intersection of Word arrays...")
    common_words = {r:1 for r in reduce(np.intersect1d, word_sets)}
    print("# of Common Words:"+str(len(common_words)))

    save_paths = []

    for we in we_list:
        '''

        lv = LargeVis(K=10,n_trees=5,max_iter=25,dim=2,M=5,gamma=7,alpha=1,rho=5)
        D = lv.fit_transform(we.X)

        df = pd.DataFrame(data=D,columns=['V1','V2'])
        df['Token'] = we.words

        print("Removing Uncommon Words")
        df = df[[w in common_words for w in df["Token"]]]
        print("Sorting DF by token")
        df.sort_values(['Token'],inplace=True)
        '''

        save_path = path+we.name+'.csv'
        #print("Saving DF to: " + save_path)
        #df.to_csv(save_path)

        save_paths.append(save_path)


    current_pardir = os.path.abspath(os.path.join(os.curdir, os.pardir))
    os.chdir(current_pardir + '/Pipeline')
    print("Launching WebBrowser...")
    webbrowser.open("http://localhost:5006/Scatter_Bokeh?webgl=1", new=1, autoraise=True)  # localhost:5006/Scatter_Bokeh
    print("Starting Server...")


    num_embs = str(len(save_paths))
    embedding_files = ' '.join(save_paths)
    #meta_data_files = '/home/nathan/Downloads/dataset7_mod.csv'


    subprocess.call(["bokeh", "serve","Scatter_Bokeh.py","--args",num_embs,embedding_files])









if __name__ == "__main__":
    launch_localhost()
