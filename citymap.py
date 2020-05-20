# Daniela Vidal Canas, Student ID: 001172091
import csv
from graph import Graph, Vertex


# Read the CSV doc and create a dictionary for each address with a nested dictionary of distances for all city addresses
def file_to_city_map_dict():
    addresses = {}
    with open("WGUPS Distance Table.csv", encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # get addresses from name column, without \n or spaces
            column_name_address = format_string_address(str(row.pop('Name')))
            str(row.pop('Address'))
            distances = {}
            for address_column, miles in row.items():
                address_for_dict = format_string_address(address_column)
                distances[address_for_dict] = miles
                addresses[column_name_address] = {
                    'Distances': distances
                }
        # fill the empty cells of the CSV
        for address_name, distances in addresses.items():
            for address, miles in distances.get('Distances').items():
                if miles == '':
                    addresses[address_name]['Distances'][address] = addresses.get(address).get('Distances').get(
                        address_name)
    return addresses


# formatter for the CSV file
def format_string_address(address_string):
    try:
        get_address = address_string[(address_string.index('\n') + 1):]
    except ValueError:
        get_address = address_string
    address_as_name_no_scape = get_address.replace('\n', '')
    if str(address_as_name_no_scape).startswith(' '):
        address_as_name_no_scape = address_as_name_no_scape[1:]
    if str(address_as_name_no_scape).endswith(' '):
        address_as_name_no_scape = address_as_name_no_scape[:-1]
    return address_as_name_no_scape


# Create a weighted graph with file information of city map
def city_map():
    global start_vertex
    global city_grid
    addresses = file_to_city_map_dict()
    city_grid = Graph()
    vertex_array = []
    names_array = []

    for name, elements in addresses.items():  # create all the vertex
        measure_vertex = Vertex(name)
        city_grid.add_vertex(measure_vertex)
        vertex_array.append(measure_vertex)
        names_array.append(name)
        if name == '4001 South 700 East, Salt Lake City, UT 84107':  # HUB address
            start_vertex = measure_vertex

    for i in range(len(vertex_array)):  # add adjacency and weight of the travel
        for j in range(len(vertex_array)):
            weight = addresses[names_array[i]]['Distances'][names_array[j]]
            city_grid.add_undirected_edge(vertex_array[i], vertex_array[j], weight)

    return city_grid, start_vertex
