# Reference 1: https://www.youtube.com/watch?v=W9XjRYFkkyw --- pandas tutorials
# Reference 2: Mentor: Chris Smit

from operator import attrgetter
import numpy
import pandas as pd
from tabulate import tabulate


# ========The beginning of the class==========
class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    def get_cost(self):
        print(f"Cost: {self.cost}")
        '''
        Add the code to return the cost of the shoe in this method.
        '''

    def get_quantity(self):
        print(f"Quantity: {self.quantity}")
        '''
        Add the code to return the quantity of the shoes.
        '''

    def __str__(self):
        print(f"""\n
Country: {self.country}
Code: {self.code}
Product: {self.product}
Cost: R{self.cost}
Quantity: {self.quantity}""")

        '''
        Add code to return shoe object as string
        '''


# Created empty shoe list for appending
shoe_list = []


# ==========Functions outside the class==============
def read_shoes_data():
    try:
        with open('inventory.txt', 'r') as shoe_file:
            data = shoe_file.readlines()

            temp_list = []  # Create temp list

            for line in data:
                temp_list.append(line)  # Append lines into list

            del temp_list[0]    # Delete line 0(headings)

            # Split lines by , to make list
            # attribute list indices to class variables
            for shoes in temp_list:
                item = shoes.split(",")
                country = item[0]
                code = item[1]
                product = item[2]
                cost = int(item[3])
                quantity = int(item[4].strip("\n"))

                # Create  variable holding all attr
                shoe_object = Shoe(country, code, product, cost, quantity)

                # Append shoe objects to shoe_list
                shoe_list.append(shoe_object)

    except FileNotFoundError as error:
        print("File not found", error)
    '''
    This function will open the file inventory.txt
    and read the data from this file, then create a shoes object with this data
    and append this object into the shoes list. One line in this file represents
    data to create one object of shoes.
    '''


# Create function for writing to file
def write_to_file():
    write_format = []
    for shoe in shoe_list:
        write_format.append(f'''{shoe.country},{shoe.code},
{shoe.product},{str(shoe.cost)},{str(shoe.quantity)}''')    # To place in format from txt file

    # Writes to txt file
    with open('inventory.txt', 'w') as file_write:
        for line in write_format:
            file_write.write(line)


# Create function to capture shoe details
def capture_shoes():
    country = input("Country: ")
    code = input("Code: ").upper()
    product = input("Product: ")
    cost = int(input("Cost: R "))
    quantity = int(input("Quantity: "))
    new_shoe = f"{country},{code},{product},{cost},{quantity}"

    # Appends shoe line to txt file
    with open('inventory.txt', 'a') as add_shoe:
        add_shoe.write("\n" + new_shoe)
    '''
    This function will allow a user to capture data
    about a shoe and use this data to create a shoe object
    and append this object inside the shoe list.
    '''


# Function to view all shoes in table format
def view_all():
    with open('inventory.txt', 'r') as shoe_data:
        shoe_list = []
        for line in shoe_data:
            line_strip = line.strip().split(",")
            shoe_list.append(line_strip)
        print(tabulate(shoe_list, headers="firstrow"))
    '''
    This function will iterate over the shoes list and
    print the details of the shoes returned from the __str__
    function. Optional: you can organise your data in a table format
    by using Python’s tabulate module.
    '''


# Function to view shoe with the lowest quantity
# Asks for amount to be restocked
# Rewrites new quantity to txt file
def re_stock():
    shoe_product = None
    quantity = 999999999
    shoe_to_restock = None

    for shoe in shoe_list:
        temp_qty = shoe.quantity
        if temp_qty < quantity:
            quantity = temp_qty
            shoe_product = shoe.product
            shoe_code = shoe.code
            shoe_to_restock = shoe

    print(f"Product: {shoe_product} \nQuantity: {quantity}")

    restock_amt = int(input("Enter new amount: "))

    shoe_to_restock.quantity = restock_amt

    restocked_list = []
    for shoe in shoe_list:
        restock_frmt = [shoe.country, shoe.code, shoe.product,
                        str(shoe.cost), str(shoe.quantity)]
        restocked_list.append(restock_frmt)

    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    restocked_list.insert(0, headers)

    # Writes to txt file
    with open('inventory.txt', 'w+') as file_write:
        for line in restocked_list:
            file_write.write(",".join([str(i) for i in line]))
            file_write.write("\n")
    '''
    This function will find the shoe object with the lowest quantity,
    which is the shoes that need to be re-stocked. Ask the user if they
    want to add this quantity of shoes and then update it.
    This quantity should be updated on the file for this shoe.
    '''


# Create function to search for shoe
# Asks user to input code.
# Iterates through shoe list
# If input == a shoe code.
# Prints shoe using __str__ method from class
# Else prints shoe does not exist
def search_shoe():
    code_input = input("Enter Shoe Code: ").upper()

    for shoe in shoe_list:
        if shoe.code == code_input:
            shoe.__str__()
            break
        else:
            continue

    if shoe.code != code_input:
        print("Shoe does not exist!")


# Create function to show value of each shoe product
# Create list for values
# Create formula for values
# Create list in format of txt file
# Append list to value list. *Because tabulate uses nested lists
# Create header and insert into list at index 0
# Print in tabular format
def value_per_item(shoe_list):
    value_list = []
    for shoe in shoe_list:
        value = shoe.quantity * shoe.cost
        list_entry = [shoe.country, shoe.code, shoe.product,
                      shoe.cost, shoe.quantity, f"R {value}"]
        value_list.append(list_entry)
    header = ["Country", "Code", "Product", "Cost", "Quantity", "Total Value"]
    value_list.insert(0, header)
    print(tabulate(value_list, headers="firstrow"))

    '''
    This function will calculate the total value for each item.
    Please keep the formula for value in mind: value = cost * quantity.
    Print this information on the console for all the shoes.
    '''


# Create function for displaying product with the highest quantity
# Used pandas function
def highest_qty():
    with open('inventory.txt', 'r') as shoes_txt:
        df = pd.read_table('inventory.txt',
                           skiprows=0,
                           sep=",",
                           )
        high_qty = df.loc[df['Quantity'].idxmax()]  # Locates maximum within 'Quantity' column
        print(high_qty.to_string())
        print("*** FOR SALE ***")


# ========== Program Starts Here ==========
# To use read data function before carrying out menu functions
read_shoes_data()

# ==========Main Menu=============


while True:
    menu = input('''Would you like to:
    --- View all --- (v)
    --- Capture new shoe data --- (c)
    --- Restock lowest quantity --- (r)
    --- Search shoe --- (s)
    --- View total value for each product --- (t)
    --- View highest quantity --- (h)
    --- Exit --- (e)
    --- > ''').lower()
    if menu == "v":
        view_all()
        print("\n")
        continue

    elif menu == "c":
        capture_shoes()
        print("\n")
        continue

    elif menu == "r":
        re_stock()
        print("\n")
        continue

    elif menu == "s":
        search_shoe()
        print("\n")
        continue

    elif menu == "t":
        value_per_item(shoe_list)
        print("\n")
        continue

    elif menu == "h":
        highest_qty()
        print("\n")
        continue

    else:
        exit()
