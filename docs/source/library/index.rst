#################
Library Reference
#################

:Release: |version|
:Date: |today|

Metadata Readers / Containers
-----------------------------
.. toctree::
   :maxdepth: 3

   unifiedmetadata
   databasemetadata
   fgdcmetadata
   gdalmetadata
   isismetadata
   plaintextmetadata
   yamlmetadata

Supported Properties
--------------------
The above readers all expose properties that should be homogenized across the library. This table contains the currently implemented properties and documents were data are being parsed from by the UnifiedMetadata object. Contributors should update this table when new metadata containers are created or when existing metadata objects have new properties added.

.. toctree::
   :maxdepth: 1

   supported_properties

Metadata Formatters
-------------------
.. toctree::
   :maxdepth: 3

   formatters/fgdcformatter
   formatters/stacformatter