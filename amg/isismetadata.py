import pvl
from shapely import wkt

class IsisMetadata():
    def __init__(self, datafile):
        self.datafile = datafile
        
    @property
    def data(self):
        if not hasattr(self, '_data'):
            self._data = pvl.load(self.datafile)
        return self._data
    
    @property
    def footprint(self):
        if not hasattr(self, '_footprint'):
            if 'Polygon' in self.data.keys():
                startbyte = self.data['Polygon']['StartByte']
                nbytes = self.data['Polygon']['Bytes']
                with open(self.datafile, 'rb') as f:
                    f.seek(startbyte-1)
                    footprint = f.read(nbytes).decode()
                    
                    self._footprint = wkt.loads(footprint)
            else:
                raise KeyError(f'Data {self.datafile} has not footprint information.')

        return self._footprint

    @property
    def longitude_domain(self):
        try:
            return self.data['IsisCube']['Mapping']['LongitudeDomain']
        except:
            return None

    @property
    def geometry(self):
        return self.footprint.__geo_interface__
    
    @property
    def bbox(self):
        return self.footprint.bounds
    
    @property
    def centroid(self):
        return self.footprint.centroid