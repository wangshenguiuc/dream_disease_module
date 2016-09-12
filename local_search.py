# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 16:41:20 2016

@author: swang141
"""
import numpy as np
import sys
import time
if len(sys.argv) not in [3]:
	print len(sys.argv)
	print 'Usage:python %s network_file result_file' % sys.argv[0]
	exit()
NETWORK_FILE = sys.argv[1]
RESULT_FILE = sys.argv[2]
#NETWORK="ppi_entrez.txt"
node_dict = {}
node_dict_rev = {}
#NETWORK_FILE = '..\\Data\\Network\\our_network\\ppi_entrez.txt'
#RESULT_FILE = '..\\Data\\Module\\local_search\\local_search.txt'
def write_cluster(result_file,assignment,node_dict_rev):
    fout = open(result_file,'w')
    ncluster = len(assignment)
    for i in range(1,ncluster+1):
        print i,len(assignment[i])
        if len(assignment[i])>=100 or len(assignment[i])<=3:
            continue
        for node in assignment[i]:
            fout.write(str(node)+'\t')
            print node
        fout.write('\n')
    fout.close()      
    
def read_graph(network_file):
    global node_dict
    global node_dict_rev
    fin = open(network_file)
    edge = {}
    node_ct = 0
    for line in fin:
        w = line.strip().split('\t')
        wt = float(w[2])
        if w[0] not in node_dict:
            node_dict[w[0]] = node_ct
            edge[node_dict[w[0]]] = {}
            node_dict_rev[node_ct] = w[0]
            node_ct+=1
        if w[1] not in node_dict:
            node_dict[w[1]] = node_ct
            edge[node_dict[w[1]]] = {}
            node_dict_rev[node_ct] = w[1]
            node_ct+=1
        edge[node_dict[w[0]]][node_dict[w[1]]] = wt
        edge[node_dict[w[1]]][node_dict[w[0]]] = wt
    print "node num",node_ct,len(node_dict_rev),node_dict_rev[node_ct-1]
    return edge,node_dict,node_dict_rev

def find_seed(network,unselected):
    nnode = len(network)    
    degree = [0.]*nnode
    for i in range(nnode):
        if i not in unselected:
            degree[i] = -1
            continue
        degree[i] = len(network[i])
    seed_priority = np.argsort(degree)[::-1]
    seed = seed_priority[0]
    w_in = 0.
    w_out = 0.
    for i in network[seed]:
        w_out += network[seed][i]
    return degree,seed_priority,w_in,w_out

def gain_add(sign,node,cluster_set,network,w_in,w_bound):
    alpha = 0.001
    w_in_new = w_in
    w_bound_new = w_bound
    #print w_in_new,w_bound_new,
    for ngh in network[node]:
        if ngh in cluster_set:
            w_in_new += network[node][ngh]*sign
            w_bound_new -= network[node][ngh]*sign
        else:
            w_bound_new += network[node][ngh]*sign
    old_gain = (w_in)/(w_in+w_bound+alpha)
    new_gain = (w_in_new) / (w_in_new + w_bound_new+alpha)
    #print w_in_new,w_bound_new
    return new_gain - old_gain, w_in_new,w_bound_new
    
    
def local_search(network):
    nnode = len(network)
    unselected = set(range(nnode))
    selected = {}
    cluster = [0]*nnode
    ncluster = 1
    weight_in = {}
    weight_bound = {}
    for ncluster in range(1,nnode):
        ##add seed
        degree,seed_priority,w_in,w_out= find_seed(network,unselected)        
        seed = seed_priority[0]
        cluster[seed] = ncluster
        unselected.remove(seed)
        selected[ncluster] = set([seed])  
        #print "seed",node_dict_rev[seed]
        weight_in[ncluster] = w_in
        weight_bound[ncluster] = w_out
        niter = 1
        old_selected = []
        while True:
            if niter>1 and old_selected == selected[ncluster]:
                break
            old_selected = selected[ncluster].copy()
            _unsel = unselected.copy()
            for i in _unsel:
                gain,w_in,w_bound = gain_add(1,i,selected[ncluster],network,weight_in[ncluster],weight_bound[ncluster])
                if gain > 0:
                    unselected.remove(i)
                    selected[ncluster].add(i)
                    weight_in[ncluster] = w_in
                    weight_bound[ncluster] = w_bound
                    cluster[i] = ncluster
                    #print "add",node_dict_rev[i],gain,len(selected[ncluster]),weight_in[ncluster],weight_bound[ncluster]
            _sel = selected[ncluster].copy()
            for i in _sel:
                gain,w_in,w_bound = gain_add(-1,i,selected[ncluster],network,weight_in[ncluster],weight_bound[ncluster])
                if gain > 0:
                    unselected.add(i)
                    selected[ncluster].remove(i)                    
                    weight_in[ncluster] = w_in
                    weight_bound[ncluster] = w_bound
                    #print "remove",node_dict_rev[i],gain,len(selected[ncluster]),weight_in[ncluster],weight_bound[ncluster]
            niter+=1
        print "iter",niter,"cluster",ncluster,"nnode",len(selected[ncluster]),"left",len(unselected)   
        if len(unselected)==0:
            break
    return selected
    
def main():
    network,node_dict,node_dict_rev = read_graph(NETWORK_FILE)
    assignment = local_search(network)
    write_cluster(RESULT_FILE,assignment,node_dict_rev)

if __name__ == '__main__':
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
