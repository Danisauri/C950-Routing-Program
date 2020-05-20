# Daniela Vidal Canas, Student ID: 001172091
# Class truck with its properties
class Truck:
    def __init__(self, truck_number):
        self.truck_number = truck_number
        self.capacity = 16
        self.speed_miles_hour = 18
        self.speed_miles_min = self.speed_miles_hour/60
        self.packages = []

    # Function to add packages at truck.packages (to load the truck)
    def add_package_to_truck(self, package):
        self.packages.append(package)
