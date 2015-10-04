#!/usr/bin/python
# -*- coding: utf-8 -*-

import csv
import networkx as nx
import geojson
from geojson import LineString, Feature, FeatureCollection

graph = nx.Graph()

with open('roads-nodes.csv', 'rb') as csvfile:
	nodes = csv.reader(csvfile, delimiter=',')
	next(nodes)
	for node in nodes:
		graph.add_node(int(node[0]), latitude=float(node[1]),longitude=float(node[2]))

with open('roads-edges3.csv', 'rb') as csvfile:
	edges = csv.reader(csvfile, delimiter=',')
	next(edges)
	for edge in edges:
		wkt = ', '.join(edge[10::])
		if 16 - float(edge[0]) <0:
			print 16 - float(edge[0])
		graph.add_edge(int(edge[2]), int(edge[3]), IndiQuiet=16-float(edge[0]), length=float(edge[4]),car=int(edge[5]),carReverse=int(edge[6]),bike=int(edge[7]),bikeReverse=int(edge[8]),foot=int(edge[9]),wkt=wkt)

# nx.write_gexf(graph, "quietest-roads.gexf")

featureCollection = []
latitude = nx.get_node_attributes(graph,'latitude')
longitude = nx.get_node_attributes(graph,'longitude')

shortest = nx.shortest_path(graph, source=1446811936, target=601662226, weight='length')
length1 = 0
quietness1 = 0

for i in range(0,len(shortest)-1):
	length = graph[shortest[i]][shortest[i+1]]['length']
	length1 += length
	quietness = graph[shortest[i]][shortest[i+1]]['IndiQuiet']
	quietness1 += quietness
	source = (latitude[shortest[i]], longitude[shortest[i]])
	target = (latitude[shortest[i+1]], longitude[shortest[i+1]])
	linestring = LineString([source, target])
	feature = Feature(geometry=linestring, properties={'type':'shortest','distance':length,'quietness':quietness})
	featureCollection.append(feature)

quietness1 = quietness1/(len(shortest)-1)
print 'shortest distance is ',length1
print 'shortest quietness is ',quietness1


quietest = nx.shortest_path(graph, source=1446811936, target=601662226, weight='IndiQuiet')
length2 = 0
quietness2 = 0
for i in range(0,len(quietest)-1):
	length = graph[quietest[i]][quietest[i+1]]['length']
	length2 += length
	quietness = graph[quietest[i]][quietest[i+1]]['IndiQuiet']
	quietness2 += quietness

	source = (latitude[quietest[i]], longitude[quietest[i]])
	target = (latitude[quietest[i+1]], longitude[quietest[i+1]])
	linestring = LineString([source, target])
	
	feature = Feature(geometry=linestring, properties={'type':'quietest','distance':length,'quietness':quietness})
	featureCollection.append(feature)



quietness2 = quietness2/(len(quietest)-1)
print 'quietest distance is ',length2
print 'quietest quietness is ', quietness2

print 'quiestest is ',((length2/length1) - 1)*100,'% longer than shortest'
print 'quiestest is ',((quietness2/quietness1) - 1)*100,'% quieter than shortest'


featureCollection = FeatureCollection(featureCollection)
dump = geojson.dumps(featureCollection, sort_keys=True)
print dump