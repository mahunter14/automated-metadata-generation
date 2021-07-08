import pytest
from shapely.geometry import Polygon
import geojson

from unittest.mock import patch, PropertyMock

from amg import databasemetadata as dmd

@pytest.fixture
def database_metadata():
    return dmd.DbMetadata('fake', 'nouri', engine='faker')

@pytest.fixture
def polygon():
    return Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])

def test_bbox(database_metadata, polygon):
    with patch('amg.databasemetadata.DbMetadata.footprint', new_callable=PropertyMock) as mock_footprint:
        mock_footprint.return_value = polygon
        assert database_metadata.bbox == (0.0, 0.0, 1.0, 1.0)

def test_geometry(database_metadata, polygon):
    with patch('amg.databasemetadata.DbMetadata.footprint', new_callable=PropertyMock) as mock_footprint:
        mock_footprint.return_value = polygon
        geo_json = database_metadata.geometry
        try:
            geojson.dumps(geo_json)
        except:
            assert False

def test_centroid(database_metadata, polygon):
    with patch('amg.databasemetadata.DbMetadata.footprint', new_callable=PropertyMock) as mock_footprint:
        mock_footprint.return_value = polygon
        centroid = database_metadata.centroid
        assert centroid.x == 0.5
        assert centroid.y == 0.5