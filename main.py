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


def snap_nodes(line, nodes_collection):
    nodes = []
    for node in nodes_collection['features']:
        p = geometry.shape(node['geometry'])
        projected_p = line.interpolate(line.project(p))
        nodes.append(projected_p)
    return nodes

def sort_nodes(line, nodes):
    coords = line.coords
    sorted_nodes = []
    for i in range(2, len(coords)):
        # We only take the segment formed by 2 coords
        l = geometry.LineString(coords[i-2:i])

        dist = None
        nearest = None
        nearest_index = None
        for i in range(len(nodes)):
            n = nodes[i]
            if l.distance(n) < 1e-8:
                nearest = n
                nearest_index = i

        if nearest:
            del(nodes[nearest_index])
            sorted_nodes.append(nearest)
    return sorted_nodes

def load(edges_fc, nodes_fc):
    line = unified_segment(edges_fc)
    nodes = snap_nodes(line, nodes_fc)
    nodes = sort_nodes(line, nodes.copy())

    fig,ax = plt.subplots(1,1,sharex=True,sharey=True)

    gpd.GeoDataFrame(geometry=[line]).plot(ax=ax)
    gpd.GeoDataFrame(geometry=nodes).plot(ax=ax, color='red')

    for i in range(len(nodes)):
        coords = list(nodes[i].coords)[0]
        plt.annotate(str(i), xy=coords)

    plt.show()

if __name__ == '__main__':
    edges_filename = 'data/quito_sections.geojson'
    nodes_filename = 'data/quito_stations.geojson'

    with open(edges_filename) as edges_file, open(nodes_filename) as nodes_file:
        load(json.load(edges_file), json.load(nodes_file))
