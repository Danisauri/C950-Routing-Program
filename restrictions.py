# Daniela Vidal Canas, Student ID: 001172091
# Functions to respond to restrictions in packages


# control over adding duplicated packages
def add_package_and_add_to_id_array(package, truck):
    if package.id not in added_id_array:
        added_id_array.append(package.id)
        truck.add_package_to_truck(package)
        package.on_truck = truck.truck_number
        return


# Same address travel together on same truck, adding 'together' restriction
def verify_same_address(my_list):
    array_of_all_address = []
    array_of_address_repeated = []
    for package in my_list:
        if package.address not in array_of_all_address:
            array_of_all_address.append(package.address)
        else:
            array_of_address_repeated.append(package.address)
    for repeated_address in array_of_address_repeated:
        ids = []
        for package in my_list:
            if package.address == repeated_address:
                ids.append(package.id)
                ids_str = ', '.join(map(str, ids))
                package.delivered_with = ids_str
    return my_list


# 1. add packages with restriction of truck number
def add_package_according_to_truck_number(my_list, trucks):
    for truck in trucks:
        for package in my_list:
            truck_to_go = package.truck_constrain
            if len(truck.packages) < truck.capacity:
                if not truck_to_go == '':
                    if truck_to_go == str(truck.truck_number):
                        add_package_and_add_to_id_array(package, truck)


# 2. Add packages that must be added together
def add_packages_together(my_list, trucks, deliver_together_array=[]):
    list_with_address_verified = verify_same_address(my_list)
    # make an array with all the packages ID that must travel together
    for package in list_with_address_verified:
        delivered_with = package.delivered_with
        if not delivered_with == '':
            if package.id not in deliver_together_array:
                deliver_together_array.append(package.id)
            for ids in delivered_with.split(', '):
                if int(ids) not in deliver_together_array:
                    deliver_together_array.append(int(ids))
    # add to truck all the elements with id in the deliver_together_array, try to use truck 3 (more empty)
    for truck in trucks:
        if len(deliver_together_array) <= (truck.capacity - len(truck.packages)):
            for package in list_with_address_verified:
                if package.id in deliver_together_array:
                    add_package_and_add_to_id_array(package, truck)


# 3. add packages with a deadline that are already in the hub
def add_available_package_with_time_constrains(my_list, trucks):
    for truck in trucks:
        for package in my_list:
            if len(truck.packages) < truck.capacity:
                # If packages are delayed in arrival, leave them to truck 1
                if not package.arrival_to_hub == '' and truck.truck_number == 3:
                    add_package_and_add_to_id_array(package, truck)
                # all other packages with deadline, add the to the other trucks
                elif not package.deadline == 'EOD' and package.arrival_to_hub == '' and not truck.truck_number == 1:
                    add_package_and_add_to_id_array(package, truck)


# 4. add the packages that are left according to capacity of the trucks
def add_remaining_packages(my_list, trucks):
    # use reversed truck to leave the 1st truck with less packages and the driver able to come back sooner for the rest
    for truck in reversed(trucks):
        for package in my_list:
            if len(truck.packages) < truck.capacity:
                add_package_and_add_to_id_array(package, truck)


# Extra: create a load control list
def create_load_control_list():
    global added_id_array
    added_id_array = []
