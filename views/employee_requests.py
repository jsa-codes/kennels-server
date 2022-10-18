import sqlite3
import json
from models import Employee
from models import Location

EMPLOYEES = [
    {"id": 1, "name": "Ryan Tanay", "address": "566 Nowhere Lane", "location_id": 1},
    {"id": 2, "name": "Bryan Tanay", "address": "586 Nowhere Lane", "location_id": 2},
]


def get_all_employees():
    """Open a connection to the database"""
    with sqlite3.connect("./kennel.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute(
            """
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            l.name location_name,
            l.address location_address
        FROM Employee e
        JOIN Location l
            ON l.id = e.location_id               
        """
        )

        # Initialize an empty list to hold all animal representations
        employees = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an employee instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # Employee class above.

            employee = Employee(
                row["id"], row["name"], row["address"], row["location_id"]
            )

            location = Location(
                row["id"], row["location_name"], row["location_address"]
            )
            
            employee.location_id = location.__dict__
            

            employees.append(employee.__dict__)

        return json.dumps(employees)


def get_single_employee(id):
    """Open a connection to the database"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Use a ? parameter to inject a variable's value
        # into the SQL statement.
        db_cursor.execute(
            """
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM Employee e
        WHERE e.id = ?
        """,
            (id,),
        )

        # Load the single result into memory
        data = db_cursor.fetchone()

        # Create an employee instance from the current row
        employee = Employee(
            data["id"], data["name"], data["address"], data["location_id"]
        )

        return employee.__dict__


def get_employee_by_location(location_id):
    """Open a connection to the database"""
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute(
            """
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.location_id = ?           
        """,
            (location_id,),
        )

        employees = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            employee = Employee(
                row["id"], row["name"], row["address"], row["location_id"]
            )
            employees.append(employee.__dict__)

    return employees


def create_employee(employee):

    max_id = EMPLOYEES[-1]["id"]

    new_id = max_id + 1

    employee["id"] = new_id

    EMPLOYEES.append(employee)

    return employee


def delete_employee(id):
    # Initial -1 value for employee index, in case one isn't found
    employee_index = -1

    # Iterate the EMPLOYEES list, but use enumerate() so that you
    # can access the index value of each item
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the employee. Store the current index.
            employee_index = index

    # If the employee was found, use pop(int) to remove it from list
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)


def update_employee(id, new_employee):
    # Iterate the EMPLOYEES list, but use enumerate() so that
    # you can access the index value of each item.
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            # Found the employee. Update the value.
            EMPLOYEES[index] = new_employee
            break
