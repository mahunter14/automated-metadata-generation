import warnings

class UnifiedMetadata():
    def __init__(self, sources, overrides={}, mappings={}):
        self.sources = sources
        self.overrides = overrides            
        self.mappings = mappings
        
    def __getattr__(self, attr):
        # If we override the attribute, get the override        
        if attr in self.overrides:
            return self.overrides[attr]
        
        # If the user explicitly defines where the data comes from, return that
        if attr in self.mappings.keys():
            for source in self.sources:
                if isinstance(source, self.mappings[attr]):
                    return getattr(source, attr)
        
        # If the user has not defined where the data comes from, seek for it
        values = {}
        for source in self.sources:
            if hasattr(source, attr):
                value = getattr(source, attr)
                values[source] = value
        
        # If more than one source delivers a piece of metadata, alert the user.
        if len(values) > 1:
            warnings.warn(f'Able to find the attribute "{attr}" in more than one data source. The user should get this value explicitly using the mapping kwarg. The values are: {values}.')
        elif len(values) == 0:
            warnings.warn(f'Unable to find the attribute "{attr}" in any data source.')
            return None
        else:
            return values[list(values.keys())[0]]