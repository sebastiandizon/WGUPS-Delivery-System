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
        self.delivery_status = 'At hub'

    def __str__(self):
        return 'ID: %s,  Address: %s, %s, %s %s,  Deadline: %s  Weight: %s  Delivery status: %s  Delivery Time: %s' % (self.package_id, self.address, self.city, self.state, self.zip, self.deadline, self.kilo_mass, self.delivery_status, self.delivery_time)