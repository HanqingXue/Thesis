#coding=utf-8
'''
seeds = open('seed.csv', 'r')
mapper = open('pathway_NO_ID.csv', 'r')

seed_list = []
mapper_dict = {}

for seed in seeds:
	if len(seed) != 0:
		seed = seed.split(',')
		seed_list.append(seed[1])

for item in mapper:
	item = item[:-1].split(',')
	key =  item[1][:-4]
	value =  item[0]
	mapper_dict[key] = value

data = open('mapper.txt', 'w')
for seed in seed_list:
	name = mapper_dict[seed]
	print seed + '\t' + name
	data.write(seed + '\t' + name + '\n')
data.close()
	#f = open('{0}.edgelist'.format(name), 'r')
'''

f = open('report.csv', 'r')
deg = []
topo = []
bc = []
count = 0
nc = []
for item in f.readlines():
	if count == 0:
		count += 1
		continue
	item = item.split(',')
	nc.append(float(item[-2]))
	topo.append(float(item[-3]))
	bc.append(float(item[-1]))


def sub(a):
	return a - min(nc)

def div(a):
	return a /(max(nc) - min(nc))
Max = max(nc)
Min = min(nc)

sub =  map(sub, nc)
div = map(div, nc)
print div
'''
result = open('clustering_count.csv', 'w')


r = {}
for item in deg:
	key =  int(item * 100) / 10


	if key in r.keys():
		r[key] += 1
	else:
		r[key] = 1


for u, v in r.items():
	result.write(str(u) +',' +str(v)  + '\n')

result.close() 
'''	 

import numpy as np    
import matplotlib.pyplot as plt    
import pandas as pd  

data = pd.DataFrame({"Betweenness Centrality": bc,
					"Topological Centrality": topo,
					"Closeness Centrality": div
					#"nc": nc
					})  
data.boxplot()#这里，pandas自己有处理的过程，很方便哦。  
plt.ylabel("ARI")  
#plt.xlabel("Dissimilarity Measures")#我们设置横纵坐标的标题。  
plt.show()  
