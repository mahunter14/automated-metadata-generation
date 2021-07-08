import datetime
import json
import os
import string
import sys

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
        item.ext.projection.centroid = {'lat':cnt.y, 'lon':cnt.x}
    if obj.extent_y and obj.extent_x:
        item.ext.projection.shape = [obj.extent_y, obj.extent_x]
    if obj.geotransform:
        item.ext.projection.transform = obj.geotransform

def populate_assets(assets, obj):
    asset_objs = {}
    for asset in assets:
        for key, value in asset.items():
            try:
                substitution_keys = [s[1] for s in string.Formatter().parse(value) if s[1] is not None]
                if substitution_keys:
                    substitution_kwargs = {k:getattr(obj, k) for k in substitution_keys}
                    asset[key] =  value.format(**substitution_kwargs)
            except:
                pass
        asset_objs[asset['key']] = pystac.Asset.from_dict(asset)

    return asset_objs

def check_geometry_size(footprint):
    """
    Excessive large geometries are problematic of AWS SQS and cause 
    performance issues becuase they are stored in plain text in the JSON
    blob.
    """
    geojson = footprint.__geo_interface__
    as_str = json.dumps(geojson)
    geomsize = len(as_str.encode('utf-8'))
    n_iterations = 0
    while geomsize > 125000:
        footprint = footprint.simplify(0.01)
        geojson = footprint.__geo_interface__
        as_str = json.dumps(geojson)
        geomsize = len(as_str.encode('utf-8'))
        n_iterations += 1
    return geojson

def to_stac(obj, 
            extensions=[pystac.Extensions.PROJECTION,
                        pystac.Extensions.DATACUBE],
            assets={},
            collection=None):    
    
    properties = {}
    
    # Base item
    dt = None
    if obj.start_date == obj.stop_date:
        dt = obj.start_date
        if not isinstance(dt, (datetime.datetime)):
            if len(dt) == 4:
                dt = datetime.datetime(int(dt), 1, 1)
            elif len(dt) == 8:  # Support ISO YYYYMMDD format
                dts = dt[0:4], dt[4:6], dt[6:]
                dt = datetime.datetime(*map(int, dts))                
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
    
    geometry = check_geometry_size(obj.footprint)

    item = pystac.Item(id=obj.productid, 
                       geometry=geometry, 
                       bbox=obj.bbox,  
                       datetime=dt,
                       stac_extensions=[pystac.Extensions.PROJECTION,
                                       pystac.Extensions.DATACUBE],
                       href=os.path.join(obj.href,f'{obj.productid}.json'),
                       collection=collection,
                       properties=properties)
    
    # Populate the projection extension
    populate_projection_extension(item, obj)
    
    # Populate the data cube extension.
    populate_datacube_extension(item, obj)
    
    #Populate the assets in the item using the passed assets dict
    assets = populate_assets(assets, obj)
    item.assets = assets

    return item
