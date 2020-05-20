# Daniela Vidal Canas, Student ID: 001172091
import csv
import math
import restrictions
import citymap
from datetime import timedelta
from graph import Vertex
from truck import Truck
from hashtable import LinearProbingHashTable
from driver import Driver
from package import Package

city_grid, start_vertex = citymap.city_map()


# Read the CSV doc and create a hash table with package information as dictionaries
def create_packages():
    with open("WGUPS Package File.csv", encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        hash_list = LinearProbingHashTable()
        for row in reader:
            package = Package(row)
            hash_list.insert(package)
    return hash_list


# Function to create instances of the truck according to how much exists as assumption
def create_trucks(available_trucks=3):
    trucks = []
    for i in range(1, (available_trucks + 1)):
        trucks.append(i)
        trucks[i - 1] = Truck(i)
    return trucks


# Function to create instances of the drivers according to how much exists as assumption
def create_drivers(available_drivers=2):
    drivers = []
    for i in range(1, (available_drivers + 1)):
        drivers.append(i)
        drivers[i - 1] = Driver(i, start_vertex)
    return drivers


# Assign available drivers to trucks and if out of drivers, get which trucks are without one driver
def assign_driver_truck(driver_array, truck_array):
    trucks_without_driver = []
    assignation_driver_truck = {}
    for i in range(len(driver_array)):
        assignation_driver_truck[driver_array[i]] = truck_array[i]
    if len(truck_array) > len(driver_array):
        trucks_without_driver = truck_array[len(driver_array):]
    return assignation_driver_truck, trucks_without_driver


# Load trucks with packages according to restrictions on each
def load_trucks(list_of_packages, trucks):
    restrictions.create_load_control_list()
    # add packages with restriction of truck number
    restrictions.add_package_according_to_truck_number(list_of_packages, trucks)
    # add packages that must be added together
    restrictions.add_packages_together(list_of_packages, trucks)
    # add packages with a deadline that are already in the hub
    restrictions.add_available_package_with_time_constrains(list_of_packages, trucks)
    # add the packages that are left according to capacity of the trucks
    restrictions.add_remaining_packages(list_of_packages, trucks)
    return trucks


# Function to associate packages and drivers
def assign_packages_to_driver(driver, truck):
    for packages in truck.packages:
        packages.driver = driver


# function to update package status on truck
def update_package_status(package, new_status, driver):
    if new_status == 'In Hub' and not package.arrival_to_hub == '':
        new_status = 'Delayed in flight'
    package.last_status = package.delivery_status
    package.hour_of_last_update = driver.get_hours_working()
    package.delivery_status = (new_status+" at "+str(package.hour_of_last_update))


# calculate closer location from the packages left in the truck
def calculate_closer_adjacent(origin_vertex, truck, min_vertex=Vertex('')):
    min_miles = math.inf
    for packages in truck:
        vertex_of_package = city_grid.get_vertex_from_label(packages.address)
        distance_to_adjacent = float(city_grid.edge_weights.get((origin_vertex, vertex_of_package)))
        if distance_to_adjacent < min_miles:
            min_miles = distance_to_adjacent
            min_vertex = vertex_of_package
    return min_miles, min_vertex


# Use of greedy algorithm to find shortest path
def shortest_path_for_truck(vertex, truck, packages, driver, break_path):
    min_vertex = ''
    if not vertex == start_vertex:
        for package in packages:
            if package.address == vertex.label:
                update_package_status(package, "Delivered", driver)
                packages.pop(packages.index(package))
        vertex.visited = True
    if not break_path == 0:
        if driver.get_hours_working() >= break_path:
            return
    route_left = len(packages)
    if route_left == 0:
        start_vertex.visited = False
        return
    else:
        if driver.get_hours_working() > timedelta(hours=10, minutes=20):
            try:
                package_9 = look_up_package(packages, 9)
                package_9.address = '410 S State St'
                package_9.city = 'Salt Lake City'
                package_9.zip = 84111
            except Exception:
                pass
        for package in packages:
            update_package_status(package, "On Transit", driver)
        if len(packages) > 0:
            min_miles, min_vertex = calculate_closer_adjacent(vertex, packages)
            driver.position = min_vertex
            driver.set_miles_traveled(min_miles)
    return shortest_path_for_truck(min_vertex, truck, packages, driver, break_path)


# Determine which driver ends first to take truck without one assigned
def get_first_free_driver(drivers, truck):
    positions = []
    available_driver = ''
    for driver in drivers:
        distance = city_grid.edge_weights.get((start_vertex, driver.position))
        positions.append(driver.minutes_passed + float(distance)/truck.speed_miles_min)
    closer_driver = min(positions)
    index_of_min = positions.index(closer_driver)
    for driver in drivers:
        if driver.driver_number == (index_of_min+1):
            available_driver = driver
    return available_driver


# Add miles of coming back to hub
def send_driver_to_hub(driver):
    distance_to_hub = city_grid.edge_weights.get((driver.position, start_vertex))
    driver.set_miles_traveled(float(distance_to_hub))


# When leaving hub late, deliver first the packages with time constrains
def get_packages_with_delivery_time(truck):
    deliver_first = []
    for package in truck.packages:
        if not package.deadline == 'EOD':
            deliver_first.append(package)
    for element in deliver_first:
        package_index = truck.packages.index(element)
        truck.packages.pop(package_index)
    return deliver_first


# Look-up function that takes package id as input and returns the corresponding data elements:
def look_up_package(my_list, key):
    for element in my_list:
        if element.id == str(key):
            return element
    return None


# Look - Up function that takes different components as input and returns the corresponding data elements
def look_up_by_component(my_list, first_filter, second_filter):
    results = []
    for element in my_list:
        if first_filter == 'id':
            if second_filter == element.id:
                results.append(element)
        if first_filter == 'address':
            if second_filter.lower() == element.address.lower():
                results.append(element)
        elif first_filter == 'deadline':
            if second_filter.lower() == element.deadline.lower():
                results.append(element)
        elif first_filter == 'city':
            if second_filter.lower() == element.city.lower():
                results.append(element)
        elif first_filter == 'zip':
            if second_filter == element.zip:
                results.append(element)
        elif first_filter == 'weight':
            if second_filter == element.weight:
                results.append(element)
        elif first_filter == 'status':
            if second_filter.lower() == element.delivery_status[0].lower():
                results.append(element)
    if len(results) == 0:
        print("No elements were found with", first_filter, "=", second_filter)
        return
    return results


# Main function
def deliver(break_path=0, my_filter=0):
    driver = ''
    packages_list = my_filter
    if filter == 0:
        packages_list = create_packages().table
    drivers = create_drivers()
    for package in packages_list:
        update_package_status(package, 'In Hub', drivers[0])
    trucks = create_trucks()
    loaded_trucks = load_trucks(packages_list, trucks)
    assignation_driver_truck, trucks_without_driver = assign_driver_truck(drivers, loaded_trucks)
    for driver, truck in assignation_driver_truck.items():
        assign_packages_to_driver(driver, truck)
        shortest_path_for_truck(start_vertex, truck, truck.packages, driver, break_path)
    if len(trucks_without_driver) > 0:
        for truck in trucks_without_driver:
            available_driver = get_first_free_driver(drivers, truck)
            send_driver_to_hub(available_driver)
            assign_packages_to_driver(available_driver, truck)
            list_delivery = get_packages_with_delivery_time(truck)
            shortest_path_for_truck(start_vertex, truck, list_delivery, available_driver, break_path)
            shortest_path_for_truck(driver.position, truck, truck.packages, available_driver, break_path)
    return packages_list, drivers


# Print status of packages when asked
def print_results(my_list, break_point):
    print('----')
    for package in my_list:
        status = package.delivery_status
        if not break_point == 0 and package.hour_of_last_update > break_point:
            status = package.last_status
        print('Pckg %s (%s), Last status update: %s (Truck: %s)' %
              (package.id, package.address, status, package.on_truck))


# Print drivers final position and miles
def print_driver_position(drivers):
    total_sum = 0
    for driver in drivers:
        total_sum += driver.miles_traveled
        print('* Driver %s at %s, in %s. Miles traveled = %s' %
              (driver.driver_number, driver.get_hours_working(), driver.position.label,
               round(driver.miles_traveled, 2)))
    print('')
    print('Total miles:', round(total_sum, 2))
    print('')


# Function to validate hour selection byu the user
def hour_validation():
    hour = ''
    minute = ''
    hour_selection = input("At what time? Enter your selection in 24h format (Ex. 13:00) or EOD: ")
    if hour_selection.lower() == 'eod':
        return 23, 0
    try:
        hour_split = hour_selection.split(':')
        hour = hour_split[0]
        minute = hour_split[1]
    except Exception:
        print(hour_selection, "is not a valid hour, please enter a valid hour")
        hour_validation()
    return int(hour), int(minute)


# Validation of filter
def first_filter_validation():
    first_filter = input(" Select an option: ")
    if first_filter == '1':
        first_filter = 'id'
    elif first_filter == '2':
        first_filter = 'address'
    elif first_filter == '3':
        first_filter = 'city'
    elif first_filter == '4':
        first_filter = 'deadline'
    elif first_filter == '5':
        first_filter = 'zip'
    elif first_filter == '6':
        first_filter = 'weight'
    elif first_filter == '7':
        first_filter = 'status'
    else:
        print('Please enter a valid filter,select an option from above')
        return first_filter_validation()
    return first_filter


# User interface to select what to display:
def user_interface():
    user_option = ''
    print('****************************************************************************')
    print("Hi! I can give you the packages status, you can finish by entering \"Q\"")
    print("Please select an option: ")
    print("1 - Status of all packages")
    print("2 - Status of specific packages")
    user_option = input("Enter your selection: ")
    while not user_option.lower() == 'q':
        if user_option == '1':
            hour, minute = hour_validation()
            break_point = timedelta(hours=hour, minutes=minute)
            packages_list, drivers = deliver(break_point)
            print_results(packages_list, break_point)
            if hour == 23:
                print_driver_position(drivers)
        elif user_option == '2':
            print("By which component would you like to filter the packages?")
            print("1 - ID")
            print("2 - Address")
            print("3 - City")
            print("4 - Deadline")
            print("5 - ZIP code")
            print("6 - Weight")
            print("7 - Status")

            first_filter = first_filter_validation()

            second_filter = input("Ok! and what specific %s do you need to check? Enter here: " % first_filter)
            hour, minute = hour_validation()
            break_point = timedelta(hours=hour, minutes=minute)
            packages_list, drivers = deliver(break_point)
            filtered_packages = look_up_by_component(packages_list, first_filter, second_filter)
            print_results(filtered_packages, break_point)
            if hour == 23:
                print_driver_position(drivers)
        else:
            print("Please select a valid time,",user_option, "is not valid")
        print('****************************************************************************')
        print("Hi! I can give you the packages status, you can finish by entering \"Q\"")
        print("Please select an option: ")
        print("1 - Status of all packages")
        print("2 - Status of specific packages")
        user_option = input("Enter your selection: ")


user_interface()
