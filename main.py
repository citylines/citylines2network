import json
from shapely import geometry, ops
import geopandas as gpd

import matplotlib
matplotlib.use('TkAgg')

import matplotlib.pyplot as plt

def unified_segment(data):
    edges = []
    for element in data['features']:
        edges.append(geometry.shape(element['geometry']))

    multiline = ops.linemerge(edges)
    coords_list = [list(line.coords) for line in multiline]

    return geometry.LineString([item for sublist in coords_list for item in sublist])


def snapped_nodes(line, nodes_collection):
    nodes = []
    orig_nodes = []
    for node in nodes_collection['features']:
        p = geometry.shape(node['geometry'])
        orig_nodes.append(p)
        projected_p = line.interpolate(line.project(p))
        nodes.append(projected_p)
    return nodes

def load(edges_fc, nodes_fc):
    line = unified_segment(edges_fc)
    nodes = snapped_nodes(line, nodes_fc)

    fig,ax = plt.subplots(1,1,sharex=True,sharey=True)

    gpd.GeoDataFrame(geometry=[line]).plot(ax=ax)
    gpd.GeoDataFrame(geometry=nodes).plot(ax=ax, color='red')
    plt.show()

if __name__ == '__main__':
    edges_filename = 'data/quito_sections.geojson'
    nodes_filename = 'data/quito_stations.geojson'

    with open(edges_filename) as edges_file, open(nodes_filename) as nodes_file:
        load(json.load(edges_file), json.load(nodes_file))
