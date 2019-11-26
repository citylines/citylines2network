class Filter:
    def __init__(self, edges_fc, nodes_fc, lines=[], year=None):
        self.lines = lines
        self.year = year

        self.edges = list(filter(self._match_features, edges_fc))
        self.nodes = list(filter(self._match_features, nodes_fc))

    def _match_features(self, feature):
        props = feature['properties']

        conditions = []
        if len(self.lines):
            conditions.append(self._lines_condition(props))

        if self.year:
            conditions.append(self._year_condition(props))

        return all(conditions)

    def _lines_condition(self, props):
        f_lines = [l['line'] for l in props['lines']]
        lines = set(f_lines) & set(self.lines)
        return lines

    def _year_condition(self, props):
        return props['opening'] <= self.year and (props['closure'] is None or props['closure'] > self.year)

    def valid(self):
        return len(self.nodes) > 1 and len(self.edges) > 0
