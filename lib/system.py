import networkx

from lib.line import Line
from lib.filter import Filter

class System:
    def __init__(self, sdict, year=None, line_names=[]):
        self.sdict = sdict
        self.year = year
        self.line_names = line_names
        self.lines = self._load_lines()

        self.nodes = [node for line in self.lines for node in line.nodes]
        self.routes = [line.route for line in self.lines]

    def _load_lines(self):
        lines = []
        for l in self.sdict:
            if len(self.line_names) and not l in self.line_names:
                continue
            f = Filter(self.sdict[l]['edges'], self.sdict[l]['nodes'], year=self.year)
            if f.valid():
                line = Line(f.edges, f.nodes)
                lines.append(line)
        return lines

    def graph(self):
        graphs = [line.graph() for line in self.lines]
        return networkx.compose_all(graphs)

    def draw_graph(self, with_labels=False,node_size=50,font_size=9):
        pos = dict([(node['properties']['id'],list(node['geometry'].coords)[0]) for node in self.nodes])
        networkx.draw_networkx(
                self.graph(),
                pos,
                with_labels=with_labels,
                node_size=node_size,
                font_size=font_size
                )
