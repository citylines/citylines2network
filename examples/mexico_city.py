# -*- coding: utf-8 -*-

import json
import geopandas as gpd

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
import sys,os

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from citylines2network import Citylines2Network

def load(edges_fc, nodes_fc):
    c2n = Citylines2Network(edges_fc['features'], nodes_fc['features'])
    print(c2n.system_names())
    print(c2n.system_line_names('Sistema de Transporte Colectivo (STC)'))

    metro = c2n.system('Sistema de Transporte Colectivo (STC)', year=2015)
    metro.draw_graph()

    '''
    fig,ax = plt.subplots(1,1,sharex=True,sharey=True)
    gpd.GeoDataFrame(geometry=metro.routes).plot(ax=ax)
    geometries = [node['geometry'] for node in metro.nodes]
    gpd.GeoDataFrame(geometry=geometries).plot(ax=ax, color='red')

    for i in range(len(metro.nodes)):
        coords = list(metro.nodes[i]['geometry'].coords)[0]
        plt.annotate(str(i), xy=coords)
    '''

    plt.title('Mexico City Metro - 2015')
    plt.show()

if __name__ == '__main__':
    """
    Files can be downloaded from https://www.citylines.co/data?city=mexico-city
    """
    edges_filename = 'data/mexico-city_sections.geojson'
    nodes_filename = 'data/mexico-city_stations.geojson'

    with open(edges_filename) as edges_file, open(nodes_filename) as nodes_file:
        load(json.load(edges_file), json.load(nodes_file))
