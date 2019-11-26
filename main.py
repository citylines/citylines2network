import json
import geopandas as gpd

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import networkx

from lib.line import Line
from lib.filter import Filter

def load(edges_fc, nodes_fc):
    af = Filter(edges_fc['features'], nodes_fc['features'], lines=['a'])
    a = Line(af.edges, af.nodes)
    a_graph = a.graph()

    bf = Filter(edges_fc['features'], nodes_fc['features'], lines=['b'])
    b = Line(bf.edges, bf.nodes)
    b_graph = b.graph()

    network = networkx.compose(a_graph, b_graph)

    pos = dict([(node['properties']['id'],list(node['geometry'].coords)[0]) for node in a.nodes + b.nodes])
    networkx.draw(network,pos,with_labels=True)

    fig,ax = plt.subplots(1,1,sharex=True,sharey=True)

    gpd.GeoDataFrame(geometry=[a.route,b.route]).plot(ax=ax)
    geometries = [node['geometry'] for node in a.nodes + b.nodes]
    gpd.GeoDataFrame(geometry=geometries).plot(ax=ax, color='red')

    for line in [a,b]:
        for i in range(len(line.nodes)):
            coords = list(line.nodes[i]['geometry'].coords)[0]
            plt.annotate(str(i), xy=coords)

    plt.show()

if __name__ == '__main__':
    edges_filename = 'data/buenos-aires_sections.geojson'
    nodes_filename = 'data/buenos-aires_stations.geojson'

    with open(edges_filename) as edges_file, open(nodes_filename) as nodes_file:
        load(json.load(edges_file), json.load(nodes_file))
