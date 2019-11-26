from lib.system import System

class Citylines2Network:
    def __init__(self, edges, nodes):
        self._systems_dict = self._build_systems_dict(edges, nodes)

    def _build_systems_dict(self, edges, nodes):
        sdict = {}
        features_list = [edges, nodes]
        keys = ['edges','nodes']
        for i in range(2):
            features = features_list[i]
            key = keys[i]
            for f in features:
                for l in f['properties']['lines']:
                    system = l['system']
                    line = l['line']
                    if not system in sdict:
                        sdict[system] = {}
                    if not line in sdict[system]:
                        sdict[system][line] = {'edges':[], 'nodes':[]}
                    sdict[system][line][key].append(f)
        return sdict

    def system_names(self):
        return list(self._systems_dict.keys())

    def system_line_names(self, name):
        return list(self._systems_dict[name].keys())

    def system(self, name, year, lines=[]):
        return System(self._systems_dict[name], year=year, line_names=lines)
