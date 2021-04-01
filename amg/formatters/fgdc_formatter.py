from osgeo import osr
osr.UseExceptions()

from amg.fgdcmetadata import FGDCMetadata

fgdc_to_osr_translation = {'equirect':[
                               ('false_easting',osr.SRS_PP_FALSE_EASTING),
                               ('false_northing',osr.SRS_PP_FALSE_NORTHING),
                               ('standard_parallel',osr.SRS_PP_STANDARD_PARALLEL_1),
                               ('meridian_longitude',osr.SRS_PP_CENTRAL_MERIDIAN)],
                           'polarst':[
                               ('standard_parallel',osr.SRS_PP_LATITUDE_OF_ORIGIN),
                               [('sv_longitude',osr.SRS_PP_LONGITUDE_OF_ORIGIN),
                                ('scale_factor',osr.SRS_PP_SCALE_FACTOR)],
                                ('false_easting',osr.SRS_PP_FALSE_EASTING),
                                ('false_northing',osr.SRS_PP_FALSE_NORTHING)],
                            'orthogr':[
                                ('center_longitude',osr.SRS_PP_LONGITUDE_OF_CENTER),
                                ('center_latitude',osr.SRS_PP_LATITUDE_OF_CENTER),
                                ('false_easting',osr.SRS_PP_FALSE_EASTING),
                                ('false_northing',osr.SRS_PP_FALSE_NORTHING)]
                            }

def lookup_projection_name(name):
    """
    """
    name = name.lower()
    if 'equirectangular' in name:
        return 'equirect'
    elif 'polarstereographic' in name:
        return 'polarst'

def populate_projection_information(template, obj):
    srs = obj.srs
    
    # Get the projection name out of the SRS.
    label_projection_name = srs.GetAttrValue('PROJCS')
    
    # Attempt to parse the projection name into a known projection name and get the fields to populate
    short_name = lookup_projection_name(label_projection_name)
    fields = fgdc_to_osr_translation.get(short_name, {})
    
    # Update the template with the data from the projection
    template.projection['name'] = label_projection_name
    for field in fields:
        if isinstance(field, list):
            for subfield in field:
                val = str(srs.GetProjParm(subfield[1]))
                if val is not None:
                    template.projection[subfield[0]] = val
                    break
        else:
            template.projection[field[0]] = str(srs.GetProjParm(field[1]))

def populate_bounding_box(template, obj):

    template.bounding_box = {'east':obj.bbox[2],
                         'south':obj.bbox[1],
                         'west':obj.bbox[0],
                         'north':obj.bbox[3]}  

    if obj.longitude_domain == 360:
        # The data are in a 0-360 domain
        template.bounding_box['west'] -= 180
        template.bounding_box['east'] -= 180

    template.bounding_box = {k:str(v) for k,v in template.bounding_box.items()}
    
def populate_raster_info(template, obj):
    template.raster_info = {'dimensions':'Pixel',
                             'column_count':obj.extent_x,
                             'row_count':obj.extent_y,
                             'vertical_count':obj.extent_x,
                             'x_resolution':obj.resolution_x,
                             'y_resolution':obj.resolution_y}
    template.raster_info = {k:str(v) for k,v in template.raster_info.items()}
    
def populate_digital_forms(template, obj):
    dfs = template.digital_forms
    for df in dfs:
        df['network_resource'] = obj.href
    
def to_fgdc(obj):
    template = None
    for s in obj.sources:
        if isinstance(s, FGDCMetadata):
            template = s.data
    
    populate_projection_information(template, obj)
    populate_bounding_box(template, obj)
    populate_raster_info(template, obj)
    populate_digital_forms(template, obj)
    
    template.planar_distance_units = 'meters'
    template.online_linkages = obj.doi

    # Add the point of contact section to the template.
    
    template.validate()
    return template.serialize(use_template=False).decode()