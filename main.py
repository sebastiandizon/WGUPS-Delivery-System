# main.py
# @author Sebastian Dizon ID
# No. 004651624

import csv
import datetime

import structure
import Package
import Truck
from datetime import timedelta

#initializes package data by constructing a package object from the data, then inserts the object into the PackageData chaining hash table
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
            # package object
            p = Package.Package(p_id, p_address, p_city, p_state, p_zip, p_deadline, p_mass_kilo, p_notes)
            #insert into hash table
            PackageData.insert(int(p.package_id), p)
#initializes numeric distance data into 2d array, populating the empty opposite side by mirroring it
def load_distance_data(filename):
    # initialize and read csv
    distance_table = list(csv.reader(open(filename)))
    DISTANCE_SIZE = distance_table.__len__()
    for i in range(DISTANCE_SIZE):
        for j in range(DISTANCE_SIZE):
            if i < j:
                distance_table[i][j] = distance_table[j][i]
    return distance_table

#initializes address data from address csv, corresponds to distance data
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

#retrieves the id of the address of a package, used in searching distance matrix
def get_address_id(package_id):
    for i in range(address_dict.__len__()):
        if address_dict[i].__contains__(PackageData.search(package_id).address):
            return i

#calculates the distance between 2 packages
def distance_between(package_1, package_2):
    distance = distance_table[get_address_id(package_1)][get_address_id(package_2)]
    return float(distance)

#calculates the distance of a given package from the hub, with given id
def distance_from_hub(package_id):
    distance = distance_table[0][get_address_id(package_id)]
    return float(distance)

#retrieves the package closest to main_package, from given list of packages
def get_nearest_package(main_package, packages):
    lowest = 140
    lowest_id = 0

    for i in range(len(packages)):
        if distance_between(main_package, packages[i]) < lowest:
            if packages[i] != main_package:
                lowest = distance_between(main_package, packages[i])
                lowest_id = packages[i]

    return lowest_id

#reorders the packages in the given truck to the most optimal route based on nearest neighbor
def get_delivery_order(truck):
    delivery_order = []
    package_list = truck.packages
    closest_to_hub = 1400
    starting_package = None
    for i in range(len(package_list)):
        if distance_from_hub(package_list[i]) < closest_to_hub:
            closest_to_hub = distance_from_hub(package_list[i])
            starting_package = package_list[i]
    truck.distance_traveled += closest_to_hub

    delivery_order.append(starting_package)
    package_list.remove(starting_package)
    search_package = starting_package

    while len(package_list) >= 1:
        x = get_nearest_package(search_package, package_list)
        truck.distance_traveled += distance_between(search_package, x)
        delivery_order.append(x)
        package_list.remove(x)
        search_package = x
    truck.packages.clear()
    truck.packages = delivery_order

#converts the list of distances into time objects for calculating package delivery times and status
def get_delivery_times(delivery_order):
    times = []
    times.append(timedelta(minutes=60 * (distance_from_hub(delivery_order[0])) / 18))
    for i in range(len(delivery_order) - 1):
        time_float = 60 * (distance_between(delivery_order[i], delivery_order[i + 1]) / truck1.speed)
        time = timedelta(minutes=time_float)
        times.append(time)
    return times

#updats delivery status and delivery time of packages on given truck at user provided target time
def get_delivery_status(truck, target_time):
    delivery_times = get_delivery_times(truck.packages)
    i = 0
    packages_delivered = False
    while not packages_delivered and i < len(delivery_times):

        if target_time >= truck.delivery_time:
            if target_time < truck.delivery_time + delivery_times[i]:
                truck.delivery_time = truck.delivery_time + delivery_times[i]
                PackageData.search(truck.packages[i]).delivery_status = 'En route'
                packages_delivered = True
                i += 1
            else:
                truck.delivery_time = truck.delivery_time + delivery_times[i]
                PackageData.search(truck.packages[i]).delivery_time = truck.delivery_time
                PackageData.search(truck.packages[i]).delivery_status = 'Delivered'

                i += 1
        else:
            packages_delivered = True

#constructor for package data hash table, populated with package data
PackageData = structure.ChainingHashTable()
distance_table = load_distance_data('DistanceTable.csv')
address_dict = load_address_data('addressess.csv')
load_package_data('PackageData.csv')

#package ids that satisfy inder 140 constraint and special constraints
first = [1, 13, 14, 16, 20, 29, 30, 31, 34, 37, 40, 15, 19, 7]

second = [3, 18, 36, 38, 6, 25, 28, 32, 27, 35, 39]

third = [9, 2, 33, 4, 5, 8, 10, 11, 12, 17, 21, 22, 23, 24, 26]
#constructor for truck one, taking first list as packages, depart time at 8am, and setting the distance traveled to 0
truck1 = Truck.Truck(first, datetime.timedelta(hours=8), 0)
#constructor for truck two, taking second list as packages, depart time at 9am, and setting the distance traveled to 0
truck2 = Truck.Truck(second, datetime.timedelta(hours=9), 0)
#orders the packages based on nearest-neighbor
get_delivery_order(truck1)
get_delivery_order(truck2)

def main():
    print(PackageData.table )
    #initializes command-line interface
    print("Welcome to WGUPS Package Delivery System")
    print("To view status of deliveries, enter your desired time")

    #while loop so the program doesnt terminate program when user misinputs
    valid_input1 = False
    while not valid_input1:
        try:
            #takes user given hour, minute, and second value in order to determine delivery status at that given time
            hour = int(input("Enter an hour (0-24) : "))
            minute = int(input("Enter minute: "))
            second = int(input("Enter seconds: "))
            get_delivery_status(truck1, datetime.timedelta(hours=hour, minutes=minute, seconds=second))
            get_delivery_status(truck2, datetime.timedelta(hours=hour, minutes=minute, seconds=second))
            #truck 3 is initialized based off of the delivery results of truck1 and truck2, at provided time of user
            truck3 = Truck.Truck(third, min(truck1.delivery_time, truck2.delivery_time), 0)
            # orders the packages on truck 3
            get_delivery_order(truck3)
            #retrieves the delivery status at user provided time
            get_delivery_status(truck3, datetime.timedelta(hours=hour, minutes=minute, seconds=second))
            #ends loop to move to next user input request
            valid_input1 = True
        except ValueError:
            print('Please enter a valid number.')
    #look to keep program going if user misinputs
    valid_input2 = False
    while not valid_input2:
        one_or_all = input("Would you like to view one package, or all? (Type 'one' or 'all') ")
        #conditional to determine if single package information or all package info is desired by user
        if one_or_all == "one":
            try:
                #user inputs desired ID and then it is searched for in the table, and the package's information is printed
                package_id = input("Enter the id of the desired package. (1-40): ")
                print(PackageData.search(int(package_id)))
                valid_input2 = True
            except:
                print('Please enter a valid input.')
                #user selects all, prints all packages delivery info and status at the given time (ie. en route, delivered)
        elif one_or_all == "all":
            print('Truck one:')
            for i in range(len(truck1.packages)):
                print(PackageData.search(truck1.packages[i]))
            print('Truck two:')
            for i in range(len(truck2.packages)):
                print(PackageData.search(truck2.packages[i]))
            print('Truck three:')
            for i in range(len(truck3.packages)):
                print(PackageData.search(truck3.packages[i]))
            valid_input2 = True
        else:
            print("Not a valid input.")
    #prints total distance traveled at the end of the program regardless of single or all selection
    print("Total distance travled: %s miles" % (
            truck1.distance_traveled + truck2.distance_traveled + truck3.distance_traveled))

if __name__ == '__main__':
    main()
    print("Thank you for using WGUPS. Program will exit.")