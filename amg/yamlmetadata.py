import yaml

class YAMLMetadata():
    def __init__(self, datafile):
        self.datafile = datafile

    def __getattr__(self, name):
        try:
            return self.data[name]
        except:
            raise AttributeError

    @property
    def data(self):
        if not hasattr(self, '_data'):
            with open(self.datafile) as f:
                self._data = yaml.load(f, Loader=yaml.FullLoader)
        return self._data
    