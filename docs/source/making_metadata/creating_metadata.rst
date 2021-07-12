#######################
Creating Metadata Files
#######################

The primary purpose of this library is the creation of geospatial metadata from a collection of sources. One of those sources will be the spatial data themselves, for example a GeoTiff. The geotiff will likely not have complete metadata that is FGDC or STAC compliant. This library supportings ingesting data from other sources in order to be able to create fully specified metadata. In practice, this means that the metadata creator will have a colletion of geospatial data products, likey a FGDC XML template (see the template directory in the code base for examples), and potentially other sources of metadata (a database, a YAML file, a generic text file, etc.)

What is needed to use the library?
==================================
In order to use this library a few assumptions are made. First, you have data staged in some way and you would like to create FGDC and/or STAC metadata for those data. Second, the data have ancillary data that are staged either alongside the geospatial data or are accessible in some way. Once the data are collected, the python standard library is used to step through the data / directories / sources and this library is used to take the collected data and generate metadata.

For example, if you have a directory like so:

.. code-block::

  root/
    - fileA.tif
    - fileA_metadata.txt
    - fileA_metadata2.lbl
    - fileB.tif
    - fileB_meatadata.txt
    - fileB_metadata2.lbl

The python standard library could be used to collect the data into two sets (fileA data and fileB data). Then this library would be used to create metadata. For the remainder of this page, when describing the library, the assumption is that the inputs are from a single set (i.e., fileA). See the notebooks directory in the source for some examples where the data are being organized into logical sets.

How does this library work?
===========================
An example is worth a thousand words. This section steps through a simple example where FGDC and STAC metadata are created for a lunar digital terrain model. First, the code is presented. Then the code is explained line by line. The goal of this section is not to provide a full understanding of the library. Rather, we hope that this section presents a high level perspective on the problem the library seeks to solve.

.. code-block:: python
    :linenos:

    fgdc = FGDCMetadata('kaguyatc_dtm_template.xml', proj='orthogr')
    gd = GDALMetadata('my_geotiff.tif')
    vrt = PcAlignMetadata('my_pcalign_output.txt')
    yml = YAMLMetadata('kaguyadtm.yml')
    
    dtm_record = UnifiedMetadata([fgdc, gd, vrt, yml])
    
    to_fgdc(dtm_record)  # Serialize to FGDC string 
    to_stac(dtm_record)  # Serialize to STAC dict (json)

In this example, lines 1-4 are reading in four different input data sources. These are data files that provide information
used to create a UnifiedMetadata object. The input sources in this example are an FGDC template (line 1), a GeoTiff (line 2), 
a plain text file that has been generated by the NASA Ames Stereo pipeline(line 3), and a YAML (line 4) file. These four different data sets provide information needed to create both FGDC and STAC metadata.
    
.. warning::
    If one were to run the example above, they would immediately see that geometry information, that comes from a database is missing. The database connection is being omitted for simplicity. Additionally, the above example may have key collisions. These are described below.

In line 1 also includes a `proj='orthogr'` keyword argument. This is simply indicating that the projection information has not been explicitly specified in the fgdc template. Instead, that information will be dynamically populated using metadata from other sources. The projection type (e.g., orthographic or equirectangular) has to be specified though.

In line 5, a UnifiedMetadata object is created from the inputs. This is a data container that provides access to the homogenized information in all of the inputs. What does that mean? 

.. note::

  The GeoTiff that is being provided exposes a bounding box via very specific syntax. In fact, the bounding box could be accessed as `data.bounding_box` or `data.bbox` or it could be derived from a geometry such as `data.footprint.bbox`. These are a collection of different access methods for the same information. Each of the data containers on lines 1-4 exposes the data using a unified set of keys. See :ref:`supported_properties` for the current listing of keys. 

The UnifiedMetadata object is then an accessor to all of the data in the library. `UnifiedMetadata.bbox` will look through all of the homogenized data source to find a `bbox` that is used to generate a metadata file.

Finally, lines 8 and 9 serialize the UnifiedMetadata object to a string or dict (respectively) using one of the available data formatters.

Examples
========
Examples are worth a thousand words. The library ships with a number of Jupyter notebooks that have been used to create and validate FGDC and STAC metadata.
