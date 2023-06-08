# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
import gspread
from google.oauth2.service_account import Credentials 
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from user
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("Data is valid!")
            break
    return sales_data

def validate_data(values):
    """
    Check if there is 6 values and check the data can be integers
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values require, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
    """
    Calculate the surplus
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    #stock_row = stock[len(stock)-1]
    stock_row = stock[-1]
    surplus_data =[]
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    return surplus_data  


def update_surplus_worksheet(data):
    """
    Update Surplus worksheet
    """
    print("Updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("Surplus worksheet updated successfully.\n")

def update_worksheet(data, worksheet):
    """
    Calculate the surplus
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet is updated")


def main():
    """
    Run all program functions
    """
    data = get_sales_data()   
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data,"sales")
    calculate_surplus_data(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    print(new_surplus_data)
    update_worksheet(new_surplus_data, "surplus")

print("Welecome to Love Sandwiches Data Automation")
main()   