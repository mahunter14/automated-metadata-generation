import json

class Provider():
    def __init__(self, name='',
                 role=None, 
                 url=None, 
                 address=None, 
                 city=None,
                 postal_code=None,
                 state=None, 
                 country=None,
                 contact_org=None,  
                 contact_person=None, 
                 email=None,
                 phone=None):
    
        self.name = name
        self.role = role
        self.url = url
        self.address = address
        self.city = city
        self.data = state
        self.postal_code = postal_code
        self.country = country
        self.contact_org = contact_org
        self.contact_person = contact_person
        self.email = email
        self.phone = phone


class Band():
    def __init__(self, 
                 bid, 
                 extent_x=None, 
                 extent_y=None,
                 values=[],
                 reference_system=None,
                 step=None,
                 unit=None):
        
        self.bid = bid
        self.extent_x = extent_x
        self.extent_y = extent_y
        self.values = values
        self.reference_system = reference_system
        self.step = step
        self.unit = unit
        
    def __repr__(self):
        attrs = {'bandid':self.bid,
                 'extent_x':self.extent_x,
                 'extent_y':self.extent_y,
                 'values':self.values,
                 'reference_system':self.reference_system,
                 'step':self.step,
                 'unit':self.unit}
        return json.dumps(attrs)