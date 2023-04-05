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
    for i in range(DISTANCE_SIZE):
        for j in range(DISTANCE_SIZE):
            if i < j:
                distance_table[i][j] = distance_table[j][i]
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
            if packages[i] != main_package:
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
        package_list.remove(x)

    return package_order


def get_route_distance(starting_index, packages):
    distance = []
    package_list = []
    for j in range(len(packages)):
        package_list.append(packages[j])

    starting_package = package_list[starting_index]
    search_package = starting_package

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
    truck.distance_traveled = lowest

    truck.packages = delivery_order


def get_delivery_times(delivery_order):
    times = []
    for i in range(len(delivery_order)-1):
        time_float = 60*(distance_between(delivery_order[i], delivery_order[i+1])/truck1.speed)
        time = timedelta(minutes=time_float)
        times.append(time)
    return times

def get_delivery_status(truck, target_time):
    delivery_times = get_delivery_times(truck.packages)

    packages_delivered = False
    index = 0

    while not packages_delivered and index < len(delivery_times):
        temp = truck.delivery_time + delivery_times[index]
        if target_time >= temp:
            if index == 0:
                PackageData.search(truck.packages[0]).delivery_time = truck.delivery_time
                PackageData.search(truck.packages[0]).delivery_status = True

            truck.delivery_time = temp
            PackageData.search(truck.packages[index+1]).delivery_time = temp
            PackageData.search(truck.packages[index+1]).delivery_status = True

        else:
            packages_delivered = True
        index += 1


PackageData = structure.ChainingHashTable()
distance_table = load_distance_data('DistanceTable.csv')
address_dict = load_address_data('addressess.csv')
load_package_data('PackageData.csv')

west_delivery_ids = [4, 5, 6, 12, 17, 19, 21, 24, 28, 31, 32, 33, 37, 40]
north_delivery_ids = [1, 3, 7, 8, 9, 10 ,13, 18, 27, 29, 30, 35, 36, 38, 39]
east_delivery_ids = [2, 11, 14, 15, 16, 20, 22, 23, 25, 26, 34]

truck1 = Truck.Truck(west_delivery_ids, datetime.timedelta(hours=9), 0)
truck2 = Truck.Truck(north_delivery_ids, datetime.timedelta(hours=8), 0)
load_and_order(truck1)
load_and_order(truck2)


def main():
    print("Welcome to WGUPS Package Delivery System")
    print("To view status of deliveries, enter your desired time")
    valid_input = False
    while not valid_input:
        try:
            hour = int(input("Enter an hour (0-24) : "))
            minute = int(input("Enter minute: "))
            second = int(input("Enter seconds: "))
            valid_input = True
        except ValueError:
            print('Please enter a valid number.')


    get_delivery_status(truck1, datetime.timedelta(hours=hour, minutes=minute, seconds=second))
    get_delivery_status(truck2, datetime.timedelta(hours=hour, minutes=minute, seconds=second))


    truck3 = Truck.Truck(east_delivery_ids, min(truck1.delivery_time, truck2.delivery_time), 0)
    load_and_order(truck3)
    get_delivery_status(truck3, datetime.timedelta(hours=hour, minutes=minute, seconds=second))

    for i in range(len(truck1.packages)):
        print("PACKAGE ID: %s, DELIVERY STATUS: %s, DELIVERY TIME: %s" % (PackageData.search(truck1.packages[i]).package_id, PackageData.search(truck1.packages[i]).delivery_status, PackageData.search(truck1.packages[i]).delivery_time))
    print("\n")

    for i in range(len(truck2.packages)):
        print("PACKAGE ID: %s, DELIVERY STATUS: %s, DELIVERY TIME: %s" % (PackageData.search(truck2.packages[i]).package_id, PackageData.search(truck2.packages[i]).delivery_status, PackageData.search(truck2.packages[i]).delivery_time))
    print("\n")

    for i in range(len(truck3.packages)):
        print("PACKAGE ID: %s, DELIVERY STATUS: %s, DELIVERY TIME: %s" % (
        PackageData.search(truck3.packages[i]).package_id, PackageData.search(truck3.packages[i]).delivery_status,
        PackageData.search(truck3.packages[i]).delivery_time))
    print("Total distance travled: %s miles" % (truck1.distance_traveled + truck2.distance_traveled + truck3.distance_traveled))

if __name__ == '__main__':
    main()

