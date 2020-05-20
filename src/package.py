# Daniela Vidal Canas, Student ID: 001172091
# Class package with its properties
from driver import Driver
class Package:
    def __init__(self, package):
        self.id = package.get('Package ID')
        self.address = package.get('Address')
        self.deadline = package.get('Deadline')
        self.city = package.get('City')
        self.zip = package.get('Zip')
        self.weight = package.get('Mass')
        self.delivery_status = package.get('DeliveryStatus')
        self.hour_of_last_update = ''
        self.on_truck = ''
        self.driver = Driver(-1,'')
        self.last_status = ''
        self.truck_constrain = package.get('Truck')
        self.arrival_to_hub = package.get('Arrival to Hub')
        self.delivered_with = package.get('Delivered With')

    def __hash__(self):
        return int(self.id)
