import glob
import json
import os
from typing import Sequence

def find_file(*path: Sequence[str]) -> str:
    """
    Helper function to find a file along a given PATH.
    """
    found = find_files(*path)
    if len(found) != 1:
        return
    return found[0]

def find_files(*path: Sequence[str]) -> list:
    return glob.glob(os.path.join(*path))

def write_fgdc(path: str, fgdc_md):
    with open(path, 'w') as f:
        f.write(fgdc_md)
    
def write_stac(path, stac_md):
    with open(path, 'w') as f:
        json.dump(stac_md.to_dict(), f, indent=2)

# TODO: Homogenize providers internal to amg
"""class Provider():
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

#TODO: HOmogenize band information
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
        return json.dumps(attrs)"""