import json
import geopandas as gpd

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import networkx

from lib.system import System

def build_systems_dict(edges, nodes):
    sdict = {}

    features_list = [edges, nodes]
    keys = ['edges','nodes']
    for i in range(2):
        features = features_list[i]
        key = keys[i]
        for f in features:
            for l in f['properties']['lines']:
                system = l['system']
                line = l['line']
                if not system in sdict:
                    sdict[system] = {}
                if not line in sdict[system]:
                    sdict[system][line] = {'edges':[], 'nodes':[]}
                sdict[system][line][key].append(f)

    return sdict

def load(edges_fc, nodes_fc):
    sdict = build_systems_dict(edges_fc['features'], nodes_fc['features'])
    print('Systems:')
    print(list(sdict.keys()))

    subte = System(sdict['Subte'], year=2019)

    pos = dict([(node['properties']['id'],list(node['geometry'].coords)[0]) for node in subte.nodes])
    networkx.draw(subte.graph(),pos,with_labels=True)

    fig,ax = plt.subplots(1,1,sharex=True,sharey=True)

    gpd.GeoDataFrame(geometry=subte.routes).plot(ax=ax)
    geometries = [node['geometry'] for node in subte.nodes]
    gpd.GeoDataFrame(geometry=geometries).plot(ax=ax, color='red')

    for i in range(len(subte.nodes)):
        coords = list(subte.nodes[i]['geometry'].coords)[0]
        plt.annotate(str(i), xy=coords)

    plt.show()

if __name__ == '__main__':
    edges_filename = 'data/buenos-aires_sections.geojson'
    nodes_filename = 'data/buenos-aires_stations.geojson'

    with open(edges_filename) as edges_file, open(nodes_filename) as nodes_file:
        load(json.load(edges_file), json.load(nodes_file))
