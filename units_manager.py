
class UnitsManager(object):
    def __init__(self):
        self.units = {} # unit-id to unit-object
        self.free_unit_id = 0 # the next unit id that will assign
    
    def register_unit(self, unit):
        unit_id = self.free_unit_id
        self.free_unit_id+=1
        self.units[unit_id] = unit
        return unit_id
        
    def unregister_unit(self, unit_id):
        return self.units.pop(unit_id)
        
    
# every unit have to inherit from this class    
class Unit(object):
    def __init__(self):
        pass