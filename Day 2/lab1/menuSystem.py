import re
import os
from dataBase import *
from classes import *

string = r'[a-zA-Z\s]+$'
emailReg = r'^[a-zA-z0-9]+@[a-z]+.[a-z]{2,4}$'


def check_office_name(name):
    cont = mysqlconnect()
    mycursor = cont.cursor()
    mycursor.execute(
        "SELECT * FROM office WHERE name = '" + name + "'")
    myresult = mycursor.fetchall()
    if(myresult):
        return False
    else:
        return True


def check_employee():
    emp_id = input("Enter Id : ")
    cont = mysqlconnect()
    mycursor = cont.cursor()
    mycursor.execute(
        "SELECT * FROM employee WHERE id = " + str(emp_id))
    myresult = mycursor.fetchall()
    if(len(myresult) == 0):
        return False
    else:
        return True


def check_employeeWithoutID(emp_id):
    cont = mysqlconnect()
    mycursor = cont.cursor()
    mycursor.execute(
        "SELECT * FROM employee WHERE id = " + str(emp_id))
    myresult = mycursor.fetchall()
    if(len(myresult) == 0):
        return False
    else:
        return True


def add_employee():
    email = input("Enter your Email : ")
    if not (re.match(emailReg, email)):
        print('invalid email')
        return

    workmood = input("Enter your Workmood : ")

    salary = input("Enter your Salary : ")
    if(int(salary) < 1000):
        print('salary is too low, it must be 1000 or more')
        return
    is_manager = input("If Manager press 1, if not press 0 : ")
    employee = Employee(email, workmood, int(
        salary), is_manager)
    office = Office(1)
    office.hire(employee)
    print('Employee added')


def delete_employee():
    emp_id = input("Enter Id : ")
    if(check_employeeWithoutID(emp_id)):
        Employee.fire_employee(emp_id)
        print('deleted')
    else:
        print('Employee does not exist')


def get_all_employees():
    employees = Office.get_all_employees()
    for i in employees:
        print("Id : ", i[0])
        print("Email : ", i[1])
        print("WorkMood : ", i[2])
        print("Salary : ", i[3])
        print("Is Manager : ", i[4])
        print("----------------------------------")


def get_employee():
    emp_id = input("Enter Id : ")
    if(check_employeeWithoutID(emp_id)):
        employees = Office.get_employee(emp_id)
        print("Id : ", employees[0][0])
        print("Email : ", employees[0][1])
        print("WorkMood : ", employees[0][2])
        print("Salary : ", employees[0][3])
        print("Is Manager : ", employees[0][4])
        print("----------------------------------")
    else:
        print('Employee does not exist')


def print_menu():
    print("to hire employee press 1")
    print("------------------------")
    print("to fire employee press 2")
    print("------------------------")
    print("to display all employees press 3")
    print("------------------------")
    print("to display employee by id press 4")
    print("------------------------")
    print("to exit press Q")


def menu():
    print_menu()
    ch = input("Enter your choice: ")
    while(ch != 'Q'):
        os.system('cls')
        if(ch == '1'):
            add_employee()
        elif(ch == '2'):
            delete_employee()
        elif(ch == '3'):
            get_all_employees()
        elif(ch == '4'):
            get_employee()
        else:
            print("Invalid Choice")
        print_menu()
        ch = input("Enter your Choice: ")


menu()
