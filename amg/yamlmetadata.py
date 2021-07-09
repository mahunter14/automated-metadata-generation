import yaml

class YAMLMetadata():
    """
    This class supports arbitrary yaml encoded metadata.
    
    Instead of providing explicit properties to every 
    attribute that this class could have, a generic
    __get__ magic method is provided that tries to 
    pull the named attribute from this data container.
    
    Parameters
    ----------
    datafile : str
               Path to the datafile to be parsed

    Attributes
    ----------
    data : str
           The path to the input data file
    """

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
    