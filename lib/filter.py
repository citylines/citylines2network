class Filter:
    def __init__(self, edges_fc, nodes_fc, lines=[]):
        self.lines = lines

        self.edges = filter(self._match_lines, edges_fc)
        self.nodes = filter(self._match_lines, nodes_fc)

    def _match_lines(self, feature):
        f_lines = [l['line_url_name'] for l in feature['properties']['lines']]
        return set(f_lines) & set(self.lines)
