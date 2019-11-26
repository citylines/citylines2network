class Filter:
    def __init__(self, edges_fc, nodes_fc, lines=[], year=None):
        self.lines = lines
        self.year = year

        self.edges = []
        self.nodes = []

        if year:
            self.edges += filter(self._match_year, edges_fc)
            self.nodes += filter(self._match_year, nodes_fc)

        if len(lines) >0:
            self.edges += filter(self._match_lines, edges_fc)
            self.nodes += filter(self._match_lines, nodes_fc)

    def _match_lines(self, feature):
        f_lines = [l['line_url_name'] for l in feature['properties']['lines']]
        return set(f_lines) & set(self.lines)


    def _match_year(self, feature):
        props = feature['properties']
        return props['opening'] <= self.year and (props['closure'] is None or props['closure'] > self.year)
