from sklearn.cluster import KMeans
from collections import defaultdict

def main():
    """

    :return:
    """
    #TODO implement test for basic clustering
    print()


class Basic_cluster_model:

    def __init__(self,n_clusters):
        """

        :param graph:
        :param matrix:
        :param n_clusters:
        """
        self.n_clusters = n_clusters


    def fit_predict(self,graph,matrix):
        """

        :param graph:
        :param matrix:
        :return:
        """
        self.graph = graph

        model = KMeans(n_clusters=self.n_clusters)
        cluster_labels = model.fit_predict(matrix)

        cluster_dict = defaultdict(list)

        for i,x in enumerate(cluster_labels):
            cluster_dict[x].append(self.graph.int_2_id[i])

        self.cluster_dict = cluster_dict


    def save(self,outfile,mode='dream'):
        """

        :param outfile:
        :return:
        """
        confidence = str(1.0)


        with open(outfile,mode='w') as f:
            counter = 1
            for cluster in self.cluster_dict:

                if mode == 'dream':
                    f.write(str(counter)+'\t'+confidence+'\t'.join([str(node) for node in self.cluster_dict[cluster]])+'\n')
                elif mode == 'pascal':
                    f.write(str(counter) + '\t' + str(counter) + '\t'.join([str(node) for node in self.cluster_dict[cluster]]) + '\n')
                counter += 1




def read_module_file(module_file):
    """

    :param module_file:
    :return:
    """

    mdict = defaultdict(list)

    counter = 1
    with open(module_file,mode='r') as f:
        for module_line in f:


            module_list = module_line.translate(None,'\n').split('\t')

            if len(module_list) < 3:
                #print('Ignoring Module with too few genes')
                pass
            else:
                m_id = module_list[0]
                m_confidence = module_list[1]
                genes = [int(g.translate(None,'\r\n')) for g in module_list[2:]]
                mdict[m_id] = genes
                #print('Module # '+str(m_id))
                #print('\tConfidence: '+str(m_confidence))
                #print('\tGenes'+str(genes))

    return mdict















if __name__ == "__main__":
    main()