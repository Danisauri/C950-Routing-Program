# Daniela Vidal Canas, Student ID: 001172091
from datetime import timedelta
from truck import Truck


# Class driver with its properties
class Driver:
    def __init__(self, driver_number, position, hour_of_start=timedelta(hours=8, minutes=0)):
        self.hour_of_start = hour_of_start
        self.driver_number = driver_number
        self.miles_traveled = 0
        self.minutes_passed = 0
        self.position = position

    # Function to set how much a driver has traveled on each movement
    def set_miles_traveled(self, miles):
        self.miles_traveled += miles

    # Function to get the time according to velocity of the truck and miles traveled
    def get_hours_working(self):
        self.minutes_passed = self.miles_traveled/Truck(-1).speed_miles_min
        hours = int(self.minutes_passed / 60)
        minutes_left = self.minutes_passed % 60
        new_hour = self.hour_of_start + timedelta(hours=hours, minutes=minutes_left)
        return new_hour
