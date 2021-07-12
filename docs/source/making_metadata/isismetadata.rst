ISIS Metadata
=============

The IsisMetadata container is quite straight forward. An ISIS cube file can be the input data source. For a full listing of the available properties on an IsisMetadataObject see :ref:`code_isismetadata`.

The IsisFootPrintBlob container is potentially more interesting. In use, it can be excessive to ship Isis cubes (that have metadata that one wants) AND GeoTiffs (that are the final data product to be shared with users). Luckily, it is quite easy to dump the ISIS cube's label (which can the be used with gthe IsisMetadata) object or a blob of data not contained in the label. For example, using the ISIS command `blobdump`, one can dump the footprint that is the ingestable using the IsisFootPrintBlob container.

.. code-block:: bash

  blobdump name=footprint type=polygon
  
