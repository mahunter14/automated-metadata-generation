import pvl
from shapely import wkt

class IsisGeomBase():
    @property
    def geometry(self):
        return self.footprint.__geo_interface__

    @property
    def centroid(self):
        return self.footprint.centroid
    
    @property
    def bbox(self):
        return self.footprint.bounds
    
    @property
    def footprint(self):
        if not hasattr(self, '_footprint'):
            startbyte = self.data['Polygon']['StartByte'] - 1
            stopbyte = self.data['Polygon']['Bytes']
            with open(self.datafile, 'rb') as f:
                f.seek(startbyte)
                self._footprint = wkt.loads(f.read(stopbyte).decode('UTF-8'))
        return self._footprint

class IsisFootPrintBlob(IsisGeomBase):
    def __init__(self, datafile):
        self.datafile = datafile

    @property
    def data(self):
        if not hasattr(self, '_data'):
            self._data = pvl.load(self.datafile)
        return self._data

class IsisMetadata(IsisGeomBase):

    def __init__(self, datafile):
        self.datafile = datafile
        
    @property
    def data(self):
        if not hasattr(self, '_data'):
            self._data = pvl.load(self.datafile)
        return self._data

    @property
    def longitude_domain(self):
        try:
            return self.data['IsisCube']['Mapping']['LongitudeDomain']
        except:
            return None