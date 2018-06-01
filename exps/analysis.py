#-*-coding:utf8-*-

import networkx as nx
import numpy as np
import os 

class Analysiser(object):
    def __init__(self, edges):
        self.graph = nx.Graph()
        self.graph.add_edges_from(edges)

    def degree_histogram(self):
        deg = nx.degree_histogram(self.graph)
        degdic = {}
        for i in range(len(deg)):
            degdic[i] = deg[i]
        return degdic

    def avg_clustering(self):
        avg = nx.clustering(self.graph)
        for i in avg:
            avg[i] = round(avg[i],3)
        return avg

    def shortestpath_distribute(self,cutoff = None):
        length = dict(nx.all_pairs_shortest_path_length(self.graph,cutoff))
        pathdictr = {}
        for i in length.keys():
            for j in length.get(i).keys():
                index = length.get(i).get(j)
                pathdictr[index] = pathdictr[index] + 1 if pathdictr.has_key(index) else 1
        return pathdictr

    def topo_distribute(self, edges):
        G = nx.Graph()
        G.add_edges_from(edges)
        length = dict(nx.all_pairs_shortest_path_length(G,2))
        topodictr = {}
        for source in length.keys():
            j = 0
            k = len(list(nx.all_neighbors(G,source)))
            if k==0 :
                topodictr[source] = 0
            else:
                num = 0
                sum = 0
                for target in length.get(source).keys():
                    if target!=source:
                        common = len(list(nx.common_neighbors(G,source,target)))
                        if target in nx.all_neighbors(G,source):
                            common += 1
                        sum += common
                        num += 1
                topodictr[source] = round(float(sum)/num/k, 3)
        return topodictr

    def neighborhood_cennectivity(self):
        neibcen = {}
        for i in nx.nodes(self.graph):
            neib = nx.all_neighbors(self.graph,i)
            sum = 0
            num = 0
            for j in neib:
                num += 1
                count = nx.all_neighbors(self.graph,j)
                sum = sum + len(list(count))
            neibcen[i] = round(float(sum)/num if num!=0 else 0, 3)
        return neibcen

    def neighborhood_distribute(self):
        neibdistr = {}
        for i in range(nx.number_of_nodes(self.graph)):
            neibdistr[i] = 0
        for i in nx.nodes(self.graph):
            index = len(list(nx.all_neighbors(self.graph,i)))
            neibdistr[index] += 1
        return neibdistr

    def closeness_centrality(self):
        clos = nx.closeness_centrality(self.graph)
        for i in clos:
            clos[i] = round(clos[i],3)
        return clos

    def betweenness_centrality(self):
        bet = nx.betweenness_centrality(self.graph)
        for i in bet:
            bet[i] = round(bet[i],3)
        return bet

    def global_avg_degree(self):
        path_dis = self.degree_histogram()
        degree_sum = 0
        for key, value in path_dis.items():
            degree_sum += key * value

        return  degree_sum / sum(path_dis.values())

    def global_avg_clustering(self):
        avg_dis = self.avg_clustering()
        return sum(avg_dis.values()) / len(avg_dis.keys())

    def global_avg_shortestpath_distribute(self):
        short_path_dis = self.shortestpath_distribute() 

        avg_path = sum([key*value for key, value in short_path_dis.items() ]) / sum(short_path_dis.values())
        return avg_path

    def global_avg_topo_distribute(self, edges):
        topo_dis = self.topo_distribute(edges)
        return  sum(topo_dis.values()) / len(topo_dis.keys())

    def global_avg_neighborhood_cennectivity(self):
        nbc_dis = self.neighborhood_cennectivity()
        return sum(nbc_dis.values()) / len(nbc_dis.keys())

    def global_avg_closeness_centrality(self):
        cc_dis =  self.closeness_centrality()
        return sum(cc_dis.values()) / len(cc_dis.keys())

    def global_betweenness_centrality(self):
        bc_dis = self.betweenness_centrality()
        return sum(bc_dis.values()) / len(bc_dis.keys())

    def network_statistics(self, edges):
        return {
            'degree': round(self.global_avg_degree(), 3),
            'clustering':round(self.global_avg_clustering(), 3),
            'short_path':round(self.global_avg_shortestpath_distribute(), 3),
            'topo': round(self.global_avg_topo_distribute(edges), 3),
            'nc': round(self.global_avg_neighborhood_cennectivity(), 3),
            'cc': round(self.global_avg_closeness_centrality(), 3),
            'bc': round(self.global_betweenness_centrality(), 3)
        }

def get_statis(floder, name_id):
    f = open('./{0}/{1}'.format(floder, name_id), 'r')
    edges = []
    for item in f.readlines():
        item = item.split(' ')
        edges.append((item[0], item[1]))
    
    analysiser = Analysiser(edges)
    statis = analysiser.network_statistics(edges)
    f.close()
    return statis

def main():
    name2id = open('pathway_NO_ID.csv', 'r')
    name_mapper = {}
    for item in name2id.readlines():
        item = item.replace('\n', '')
        item = item.replace('.txt', '')
        item = item.split(',')
        key = item[0]
        name_mapper[key] = item[1]


    
    f  = open('report.csv', 'r')
    f.write('{0},{1},{2},{3},{4},{5}\n'.format(
        'Avg degree', 
        'Avg clustering', 
        'Avg short_path', 
        'Avg_topo',
        'Avg_nc',
        'Avg_cc',
        'Avg_bc'))
    for item in os.listdir('./origingraph'):
        key = item[:-9]
        name = name_mapper[key]
        stat = get_statis('origingraph', item)
        print key
        f.write('{0},{1},{2},{3},{4},{5},{6}\n'.format(
        name,
        stat['degree'], 
        stat['clustering'], 
        stat['short_path'],
        stat['topo'],
        stat['nc'],
        stat['bc'],
        stat['cc']))

    f.close()

    #analysiser.global_avg_topo_distribute(edges)
    #analysiser.global_avg_neighborhood_cennectivity()

if __name__ == '__main__':
    main()
