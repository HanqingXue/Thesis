import os

out = open('net.csv', 'w')

cancer = open('gene.txt', 'r')
cancer = [item[:-1] for item in cancer.readlines()]
print len(cancer)

for item in os.listdir('./node'):
	name = item
	f = open('./node/' +item, 'r')
	gene =  [item[:-1] for item in f.readlines()]
	ge = len(gene)
	common = len(set(gene) & set(cancer))


	if len(gene) == 0:
		s = name[:-4] + ',' +'{0},{1},{2}\n'.format(common, ge, 0)
		out.write(s)
	else:
		s = name[:-4] + ','+'{0},{1},{2}\n'.format(common, ge, round(float(common)/float(ge), 4))
		out.write(s)

	#out.write('{0},{1}\n'.format(item[:-4], l))

	f.close()

out.close()
