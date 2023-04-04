class Truck:
    def __init__(self, packages, delivery_time, distance_traveled):
        self.packages = packages
        self.max_load = 16
        self.speed = 18
        self.delivery_time = delivery_time
        self.distance_traveled = distance_traveled
        #TODO: Fill LoadedPackages table initial packages & updates the list when packages are delivered or added

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.packages, self.max_load, self.speed, self.delivery_time, self.distance_traveled)

