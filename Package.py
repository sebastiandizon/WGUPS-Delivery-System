class Package:
    def __init__(self, package_id, address, city, state, zip, deadline, kilo_mass, notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.kilo_mass = kilo_mass
        self.notes = notes
        self.delivery_time = None
        self.delivery_status = False;
    #TODO: fix __str__ to return all values eg: %s %s $(val)
    def __id__(self):
        return self.package_id
    def __str__(self):
        return 'ID: ' + str(self.package_id) + ', Address: ' + self.address
