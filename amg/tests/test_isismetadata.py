import os

import geojson
import pvl
import pytest
import shapely

from amg import isismetadata as imd

@pytest.fixture
def isis_footprintblob(datadir):
    return imd.IsisFootPrintBlob(os.path.join(datadir, 'footprintblob.wkt'))

@pytest.fixture
def isis_cubelabel(datadir):
    return imd.IsisMetadata(os.path.join(datadir, 'cube.label'))


class TestIsisFootprintBlob():

    def test_data(self, isis_footprintblob):
        data = isis_footprintblob.data
        assert isinstance(data, pvl.PVLModule)

    def test_footprint(self, isis_footprintblob):
        footprint = isis_footprintblob.footprint
        assert isinstance(footprint, (shapely.geometry.polygon.Polygon,
                                    shapely.geometry.multipolygon.MultiPolygon))

    def test_geometry(self, isis_footprintblob):
        geojson_dict = isis_footprintblob.geometry
        # Test that valid geojson is coming out by serializing
        # using a third party library.
        try:
            geojson_str = geojson.dumps(geojson_dict)
        except:
            assert False

    def test_centroid(self, isis_footprintblob):
        centroid = isis_footprintblob.centroid 
        assert centroid.x == pytest.approx(138.98635)
        assert centroid.y == pytest.approx(9.40386)

    def test_bbox(self, isis_footprintblob):
        assert isis_footprintblob.bbox == (132.0375443856883, 
                                        -0.1143492780517991, 
                                        147.13550355857274, 
                                        16.668013305236155)

class TestIsisMetadata():

    def test_data(self, isis_cubelabel):
        data = isis_cubelabel.data
        assert isinstance(data, pvl.PVLModule)

    def test_longitude_domain(self, isis_cubelabel):
        assert isis_cubelabel.longitude_domain == 360

    def test_missing_longitude_domain(self, isis_cubelabel):
        data = isis_cubelabel.data
        del data['IsisCube']['Mapping']['LongitudeDomain']
        assert isis_cubelabel.longitude_domain == None