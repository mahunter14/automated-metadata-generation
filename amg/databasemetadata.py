import sqlalchemy
from shapely import wkt


class DbMetadata():
    def __init__(self, dbname, uri, sql='SELECT geom FROM images LIMIT 1;'):
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
        >>> db = DbMetadata('mars', 'postgresql://jay:abcde@autocnet.wr.usgs.gov:30001', sql=sql)
        >>> db.footprint
        """
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