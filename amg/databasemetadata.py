import sqlalchemy
from shapely import wkt


class DbMetadata():
    """
    This class connects to a database using SQLAlchemy, uses the sql kwarg
    to execute a query that returns a geometry, loads the geometry into
    a shapely geometry, and finally returns a number of metadata
    properties.

    Arguments
    ---------
    dbname : str
                The name of the database to connect to

    uri : str
            The connection string in the form 
            {databasetype}://{username}:{password}@{host}:{port}
    
    sql : str
            The sql query to execute. This query should return a 
            WKT Geometry

    engine: obj
            As an alternative to passing in the dbname and uri, it
            is possible to simply pass a fully configure SQLAlchemy
            engine object. If this is used, pass None args for dbname
            and uri.

    Attributes
    ----------
    footprint : obj
                shapely Polygon or MultiPolygon

    geometry : dict
                A dictionary containing geojson

    bbox : tuple
            Containing the four elements of the bounding box in
            the form (xmin, ymin, xmax, ymax)

    centroid : obj
                a shapely Point object defining the centroid
                of the footprint
                
    Examples
    --------
    >>> sql = '''
        WITH cte_geoms AS
            (
            SELECT id, geom FROM ctx
            WHERE 
                ctx.name LIKE ANY (array ['B17_016091_2064_XN_26N031W%%', 'P17_007718_2022_XN_22N031W%%'])
            )
        SELECT ST_AsText(ST_Extent(ST_Intersection(A.geom, B.geom))) FROM cte_geoms as A, cte_geoms as B
        WHERE A.id > B.id AND A.id != B.id'''
    >>> db = DbMetadata('dbname', 'postgresql://uname:pw@mydbrui.gov:port', sql=sql)
    >>> db.footprint
    """
    def __init__(self, dbname, uri, sql='SELECT geom FROM images LIMIT 1;', engine=None):
        if engine:
            self.engine = engine
        else:
            self.engine = sqlalchemy.create_engine(f'{uri}/{dbname}')
        self.sql = sql

    @property
    def footprint(self):
        if not hasattr(self, '_footprint'):
            with self.engine.connect() as connection:
                result = connection.execute(self.sql).fetchone()
                self._footprint = wkt.loads(result[0])
        return self._footprint

    @property
    def geometry(self):
        return self.footprint.__geo_interface__

    @property
    def bbox(self):
        return self.footprint.bounds
    
    @property
    def centroid(self):
        return self.footprint.centroid