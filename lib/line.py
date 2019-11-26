from shapely import geometry, ops
import networkx

class Line:
    def __init__(self, edges_fc, nodes_fc):
        self.route = self._build_route(edges_fc)
        nodes = self._snap_nodes(nodes_fc)

        self.nodes = self._sort_nodes(nodes)
        self.edges = self._build_edges()

    def _build_route(self, edges_collection):
        edges = [geometry.shape(f['geometry']) for f in edges_collection]

        merged = ops.linemerge(edges)

        if isinstance(merged, geometry.LineString):
            return merged
        else:
            coords_list = [list(line.coords) for line in merged]
            return geometry.LineString([item for sublist in coords_list for item in sublist])

    def _snap_nodes(self, nodes_collection):
        nodes = []
        for node in nodes_collection:
            p = geometry.shape(node['geometry'])
            projected_p = self.route.interpolate(self.route.project(p))
            new_node = {
                    'properties': node['properties'],
                    'geometry': projected_p
                    }
            nodes.append(new_node)
        return nodes

    def _sort_nodes(self, nodes):
        coords = self.route.coords
        sorted_nodes = []
        for i in range(2, len(coords)):
            # We only take the segment formed by 2 coords
            l = geometry.LineString(coords[i-2:i])

            nearest = None
            nearest_index = None
            for i in range(len(nodes)):
                n = nodes[i]
                if l.distance(n['geometry']) < 1e-8:
                    nearest = n
                    nearest_index = i

            if nearest:
                del(nodes[nearest_index])
                sorted_nodes.append(nearest)
        return sorted_nodes

    def _build_edges(self):
        nodes_geom = geometry.MultiPoint([node['geometry'] for node in self.nodes])
        return ops.split(self.route, nodes_geom)

    def graph(self):
        network = networkx.Graph()

        for i in range(len(self.nodes)):
            node = self.nodes[i]
            node_id = node['properties']['id']
            network.add_node(node_id)
            if i > 0:
                previous_node_id = self.nodes[i-1]['properties']['id']
                network.add_edge(previous_node_id, node_id)

        return network
