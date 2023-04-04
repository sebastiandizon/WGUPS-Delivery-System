# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import csv
import datetime

import structure
import Package
import Truck
from datetime import timedelta


def load_package_data(filename):
    with open(filename) as package_file:
        package_data = csv.reader(package_file, delimiter=',')
        next(package_data)
        for package in package_data:
            p_id = int(package[0])
            p_address = package[1]
            p_city = package[2]
            p_state = package[3]
            p_zip = package[4]
            p_deadline = package[5]
            p_mass_kilo = package[6]
            p_notes = package[7]
            #package object
            p = Package.Package(p_id, p_address, p_city, p_state, p_zip, p_deadline, p_mass_kilo, p_notes)
            #print(p.__str__())
            PackageData.insert(int(p.package_id), p)


def load_distance_data(filename):
    #initialize and read csv
    distance_table = list(csv.reader(open(filename)))
    DISTANCE_SIZE = distance_table.__len__()
    #fill null values in 2d matrix
    for i in range(DISTANCE_SIZE):
        for j in range(DISTANCE_SIZE):
            if i < j:
                distance_table[i][j] = distance_table[j][i]
    #print(distance_table)
    return distance_table


def load_address_data(filename):
    with open(filename) as address_file:
        address_data = csv.reader(address_file, delimiter=',')
        next(address_file)
        i = 0
        address_list = {}
        for address in address_data:
            address_list[i] = address[0]
            i += 1
    return address_list


def get_address_id(package_id):
    for i in range(address_dict.__len__()):
        if address_dict[i].__contains__(PackageData.search(package_id).address):
            return i


def distance_between(package_1, package_2):
    distance = distance_table[get_address_id(package_1)][get_address_id(package_2)]
    return float(distance)


def get_nearest_package(main_package, packages):
    lowest = 140
    lowest_id = 0

    for i in range(len(packages)):
        if distance_between(main_package, packages[i]) < lowest:
            if packages[i] !=main_package:
                lowest = distance_between(main_package, packages[i])
                lowest_id = packages[i]

    return lowest_id


def get_delivery_order(starting_index, packages):
    package_list = []
    for j in range(len(packages)):
        package_list.append(packages[j])

    starting_package = package_list[starting_index]
    search_package = starting_package
    package_order = [starting_package]

    while len(package_list) > 1:
        x = get_nearest_package(search_package, package_list)
        package_order.append(x)
        print(x)
        package_list.remove(x)

    return package_order


def get_route_distance(starting_index, packages):
    distance = []
    package_list = []
    for j in range(len(packages)):
        package_list.append(packages[j])

    starting_package = package_list[starting_index]
    search_package = starting_package
    package_order = [starting_package]

    while len(package_list) > 1:
        x = get_nearest_package(search_package, package_list)
        distance.append(distance_between(search_package, x))
        package_list.remove(x)

    return distance


def load_and_order(truck):
    truck_packages = []
    for j in range(len(truck.packages)):
        truck_packages.append(truck.packages[j])

    delivery_order = []
    lowest = 100000
    for i in range(len(truck_packages)):
        temp = sum(get_route_distance(i, truck_packages))
        if temp < lowest:
            lowest = temp
            delivery_order = get_delivery_order(i, truck_packages)

    print('path of lowest distance: %s' % (lowest))
    truck.packages = delivery_order


def get_delivery_distance(delivery_order):
    distances = []
    for i in range(len(delivery_order)-1):
        distances.append(distance_between(delivery_order[i], delivery_order[i+1]))
    return distances


def get_delivery_times(delivery_distances):
    times = []
    for i in range(len(delivery_distances)):
        times.append(60*(delivery_distances[i]/truck1.speed))
    return times

def get_deliveries(truck):
    delivery_times = [get_delivery_times(get_delivery_distance(truck.packages))]
    packages = []
    packages_delivered = False
    for i in range(len(truck.packages)):
        packages.append(PackageData.search(truck.packages[i]))

    j = 0
    while not packages_delivered:
        print(packages[j].delivery_status)
        packages_delivered = True


PackageData = structure.ChainingHashTable()
distance_table = load_distance_data('DistanceTable.csv')
address_dict = load_address_data('addressess.csv')
load_package_data('PackageData.csv')

north_delivery_ids = [33, 24, 5, 37, 28, 20, 1, 4, 19, 21, 40, 6, 32, 12, 17, 31]
east_delivery_ids = [11, 14, 15, 16, 22, 23, 25, 26, 34, 2]
west_delivery_ids = [4, 5, 6, 12, 17, 19, 20, 21, 24, 28, 31, 32, 33, 37, 40]

truck1 = Truck.Truck(north_delivery_ids, datetime.timedelta(hours=8), 0)
truck2 = Truck.Truck(east_delivery_ids, datetime.timedelta(hours=8), 0)
truck3 = Truck.Truck(west_delivery_ids, min(truck1.delivery_time, truck2.delivery_time), 0)
load_and_order(truck1)
load_and_order(truck2)
load_and_order(truck3)

print(truck1.packages)


truck3 = Truck.Truck(west_delivery_ids, min(truck1.delivery_time, truck2.delivery_time), 0)


def main():
    print("Main.py init")
    get_deliveries(truck1)

if __name__ == '__main__':
    main()

