import networkx

from lib.line import Line
from lib.filter import Filter

class System:
    def __init__(self, sdict, year=None):
        self.sdict = sdict
        self.year = year
        self.lines = self._load_lines()

        self.nodes = [node for line in self.lines for node in line.nodes]
        self.routes = [line.route for line in self.lines]

    def _load_lines(self):
        lines = []
        for l in self.sdict:
            f = Filter(self.sdict[l]['edges'], self.sdict[l]['nodes'], year=self.year)
            line = Line(f.edges, f.nodes)
            lines.append(line)
        return lines

    def graph(self):
        graphs = [line.graph() for line in self.lines]
        return networkx.compose_all(graphs)
