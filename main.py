import json
import geopandas as gpd

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import networkx

from lib.line import Line

def load(edges_fc, nodes_fc):
    line = Line(edges_fc['features'], nodes_fc['features'])

    network = line.graph()

    pos = dict([(node['properties']['id'],list(node['geometry'].coords)[0]) for node in line.nodes])
    networkx.draw(network,pos,with_labels=True)

    fig,ax = plt.subplots(1,1,sharex=True,sharey=True)

    gpd.GeoDataFrame(geometry=[line.route]).plot(ax=ax)
    geometries = [node['geometry'] for node in line.nodes]
    gpd.GeoDataFrame(geometry=geometries).plot(ax=ax, color='red')

    for i in range(len(line.nodes)):
        coords = list(line.nodes[i]['geometry'].coords)[0]
        plt.annotate(str(i), xy=coords)

    plt.show()

if __name__ == '__main__':
    edges_filename = 'data/quito_sections.geojson'
    nodes_filename = 'data/quito_stations.geojson'

    with open(edges_filename) as edges_file, open(nodes_filename) as nodes_file:
        load(json.load(edges_file), json.load(nodes_file))
