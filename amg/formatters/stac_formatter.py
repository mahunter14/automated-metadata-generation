import datetime

import pystac
from pystac.extensions.projection import ProjectionItemExt

def populate_datacube_extension(item, obj):
    xdim = {'type':'spatial',
                  'axis':'x',
                  'extent':[obj.bbox[0], obj.bbox[2]],}
    
    ydim = {'type':'spatial',
                'axis':'y',
                'extent':[obj.bbox[1], obj.bbox[3]],}
    
    item.properties['cube:dimensions'] = {'x':xdim,
                                          'y':ydim}

def populate_projection_extension(item, obj):
    item.ext.projection.epsg = obj.epsg
    
    if obj.wkt2:
        item.ext.projection.wkt2 = obj.wkt2
    if obj.projjson:
        item.ext.projection.projjson = obj.projjson
    if obj.geometry:
        # TODO: Fix geom to be valid
        #item.ext.projection.geometry = obj.geometry
        pass
    if obj.bbox:
        item.ext.projection.bbox = obj.bbox
    if obj.centroid:
        cnt = obj.centroid
        item.ext.projection.centroid = {'lat':cnt.y, 'lon':cnt.y}
    if obj.extent_y and obj.extent_x:
        item.ext.projection.shape = [obj.extent_y, obj.extent_x]
    if obj.geotransform:
        item.ext.projection.transform = obj.geotransform

def to_stac(obj, 
            extensions=[pystac.Extensions.PROJECTION,
                        pystac.Extensions.DATACUBE]):    
    
    properties = {}
    
    # Base item
    dt = None
    if obj.start_date == obj.stop_date:
        dt = obj.start_date
        if not isinstance(dt, (datetime.datetime)):
            dt = datetime.datetime(int(dt), 1, 1)
    else:
        properties['start_datetime'] = obj.start_date
        properties['stop_datetime'] = obj.stop_date
        
    # Basic
    if obj.title:
        properties['title'] = obj.title
    
    if obj.description:
        properties['description'] = obj.description
    
    #Instrument
    if obj.missions:
        properties['mission'] = ','.join(obj.missions)

    if obj.instruments:
        properties['instruments'] = obj.instruments
        
    if obj.gsd:
        properties['gsd'] = obj.gsd
    
    # License
    if obj.license:
        properties['license'] = obj.license
        
    """# Providers
    if obj.providers:
        # Step over all the providers
        # If the providers are the same, do something.
        properties['providers'] = []
        for i, provider in enumerate(obj.providers):
            properties['providers'].append({'name':provider.contact_org,
                                            'roles':[]})"""
    
    item = pystac.Item(id=obj.productid, 
                       geometry=obj.geometry, 
                       bbox=obj.bbox,  
                       datetime=dt,
                       stac_extensions=[pystac.Extensions.PROJECTION,
                                       pystac.Extensions.DATACUBE],
                       properties=properties)
    
    # Populate the projection extension
    populate_projection_extension(item, obj)
    
    # Populate the data cube extension.
    populate_datacube_extension(item, obj)
    
    return item