from gis_metadata.fgdc_metadata_parser import FgdcParser


class FGDCMetadata():
    
    def __init__(self, xmlfile):
        self.xmlfile = xmlfile
    
    @property
    def data(self):
        if not hasattr(self, '_data'):
            with open(self.xmlfile, 'r') as metadata:
                self._data = FgdcParser(metadata)
        return self._data
    
    @property
    def title(self):
        return self.data.title
    
    @property    
    def description(self):
        return self.data.abstract + self.data.purpose

    @property 
    def start_date(self):
        dates = self.data.dates
        if dates['type'] == 'range':
            return dates['values'][0]
        elif dates['type'] == 'single':
            return dates['values'][0]
        else:
            print(dates)
            raise ValueError('Driver needs to be updated to support a non-range date type')
    
    @property 
    def stop_date(self):
        dates = self.data.dates
        if dates['type'] == 'range':
            return dates['values'][1]
        if dates['type'] == 'single':
            return dates['values'][0]
        else:
            raise ValueError('Driver needs to be updated to support a non-range date type')
    
    @property 
    def updated_date(self):
        return self.data.publish_date
    
    @property 
    def license(self):
        return self.data.dist_liability
    
    @property 
    def providers(self):
        providers = []
        distribution_provider = Provider(name=self.data.dist_contact_person,
                                         role='host',
                                         address=self.data.dist_address,
                                         city=self.data.dist_city,
                                         state=self.data.dist_state,
                                         postal_code=self.data.dist_postal,
                                         country=self.data.dist_country,
                                         contact_org=self.data.dist_contact_org,
                                         email=self.data.dist_email,
                                         phone=self.data.dist_phone)
        
        providers.append(distribution_provider)
        
        if hasattr(self.data, 'contacts'):
            for contact in self.data.contacts:
                providers.append(Provider(name=contact['name'],
                                          contact_org=contact['organization'],
                                          email=contact['email']))
        
        return providers