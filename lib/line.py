from shapely import geometry, ops
import networkx

class Line:
    def __init__(self, edges_fc, nodes_fc):
        self.route = self._build_route(edges_fc)
        nodes = self._snap_nodes(nodes_fc)

        self.nodes = self._sort_nodes(nodes)
        self.edges = self._build_edges()

    def _join_edges(self, edges):
        dist_threshold = 0.0001

        for edge_idx in range(len(edges)):
            edge = edges[edge_idx]
            head = edge.coords[0]
            tail = edge.coords[-1]
            coords = [head, tail]

            for i in range(2):
                node = coords[i]
                dists = []
                for e in edges:
                    if e != edge:
                        h = e.coords[0]
                        t = e.coords[-1]
                        point = geometry.Point(node)
                        dists.append((h, point.distance(geometry.Point(h))))
                        dists.append((t, point.distance(geometry.Point(t))))

                min_dist = None
                min_point = None
                for el in dists:
                    if min_dist is None or el[1] < min_dist:
                        min_dist = el[1]
                        min_point = el[0]

                print(min_dist)
                if min_dist < dist_threshold and min_dist != 0:
                    edge_coords = list(edge.coords)
                    print("node replaced")
                    if i == 0:
                        old = edge_coords[0]
                        edge_coords[0] = min_point
                        print(old,'vs',min_point)
                    else:
                        old = edge_coords[-1]
                        edge_coords[-1] = min_point
                        print(old,'vs',min_point)
                    edges[edge_idx] = geometry.LineString(edge_coords)
        return edges

    def _build_route(self, edges_collection):
        edges = [geometry.shape(f['geometry']) for f in edges_collection]
        edges = self._join_edges(edges)
        merged = ops.linemerge(edges)

        if isinstance(merged, geometry.LineString):
            return merged
        else:
            '''
            This case is for situations were the segment sorting failed.
            It may generate wrong ouputs
            '''
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
