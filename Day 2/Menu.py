import MySQLdb
import re
import os


# email validation check


def check(email):
    emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(emailRegex, email)):
        return True
    else:
        print('Invalid Email')
        return False

def checkString(str):
    strRegex = r'[a-zA-Z\s]+$'
    if(re.fullmatch(strRegex, str)):
        return True
    else:
        return False

def checkInt(value):
    if value.isdecimal():
        return True
    else:
        return False

def connectToDB():
    con = MySQLdb.connect('localhost', 'root', '', 'python_lap2')
    return con

######## Database Tables ##############
def createEmpTable():
    con = connectToDB()
    mycursor = con.cursor()
    mycursor.execute(
        '''CREATE TABLE IF NOT EXISTS 
        employee(
            id INT AUTO_INCREMENT PRIMARY KEY, 
            email VARCHAR(30) NOT NULL, 
            workmood VARCHAR(30) NOT NULL, 
            salary int NOT NULL,
            is_manager BOOLEAN NOT NULL,
            office_id INT NOT NULL,
            reg_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, 
            FOREIGN KEY (office_id) REFERENCES office(id)
        )
    ''')

def createOfficeTable():
    con = connectToDB()
    mycursor = con.cursor()
    mycursor.execute(
        '''CREATE TABLE IF NOT EXISTS 
        office(
            id INT AUTO_INCREMENT PRIMARY KEY, 
            name VARCHAR(30) NOT NULL
        )
    ''')

# CREATE OFFICE TABLE for OFFICE CLASS
createOfficeTable()

# CREATE EMPLOYEE TABLE for PERSON CLASS
createEmpTable()


# PERSON CLASS
class Person:
    healthRate = 0

    def __init__(self, full_name, money, sleepmood, healthRate):
        self.full_name = full_name
        self.money = money
        self.sleepmood = sleepmood
        self.healthRate = healthRate

    # SLEEP METHOD
    # @ classmethod
    def sleep(self, hours):
        if hours.isdecimal():
            hours = int(hours)
            if(hours == 7):
                self.sleepmood = 'happy'
                return self.sleepmood
            elif(hours < 7):
                self.sleepmood = 'tired'
                return self.sleepmood
            else:
                self.sleepmood = 'lazy'
                return self.sleepmood
        else:
            return 'please enter values in range'

    # EAT METHOD
    # @ classmethod
    def eat(self, meals):
        if meals.isdecimal():
            meals = int(meals)
            if(meals == 3):
                self.healthRate = 100
                return self.healthRate
            elif(meals == 2):
                self.healthRate = 75
                return self.healthRate
            elif(meals == 1):
                self.healthRate = 50
                return self.healthRate
            else:
                return 'please enter values in range'
        else:
            return 'please enter a valid value'

    # BUY METHOD
    # @ classmethod
    def buy(self, items):
        if items.isdecimal():
            items = int(items)
            if(items == 1):
                self.money = self.money - 10
            else:
                return 'please enter values in range'
        else:
            return 'please enter a valid value'

# EMPLOYEE CLASS
class Employee(Person):
    id = 0
    def __init__(self, email, workmood, salary, is_manager, office_id):
        if(check(email)):
            self.email = email

        self.workmood = workmood

        # if checkInt(salary):
        if(salary < 1000):
            print('salary is too low, it must be 1000 or more')
        else:
            self.salary = salary

        self.is_manager = is_manager

        self.office_id = office_id

        self.id += 1    ## id is auto increment

    # @classmethod
    def send_email(self, to, subject, body, receiver_name):
        if not(check(to)):
            print('Invalid Email')
        elif not(checkString(subject)):
            print('Invalid Subject')
        elif not(checkString(body)):
            print('Invalid Body')
        elif not(checkString(receiver_name)):
            print('Invalid Receiver Name')
        else:
            try:     
                tempFile = open('file.txt', 'w')
                Line = [str(to), "\n", str(subject), "\n",
                        str(body), "\n", str(receiver_name)]
                tempFile.writelines(Line)
                tempFile.close()
            except:
                print('error')
            
            print('Email sent to ' + receiver_name)

    # @classmethod
    def work(self, hours):
        if(checkInt(hours)):
            if(hours == 8):
                self.workmood = 'happy'
                return self.workmood
            elif(hours > 8):
                self.workmood = 'tired'
                return self.workmood
            elif(hours < 8):
                self.workmood = 'lazy'
                return self.workmood
        else:
            return 'please enter a valid value'

# OFFICE CLASS
class Office:
    id = 0
    def __init__(self, id):
        self.office_id = id
        
    # CREATE OFFICE METHOD (C => CRUD)
    # @classmethod
    def add_office(self, name):
        self.name = name
        Office.id += 1
        self.office_id = Office.id
        # add office
        cont = connectToDB()
        mycursor = cont.cursor()
        print(self.name)
        print("name")
        mycursor.execute("INSERT INTO office(name) VALUES('" + self.name + "')")
        cont.commit()
        return 'office added'

    # READ OFFICE METHOD (R => CRUD)
    def select_office(self):
        # select office
        cont = connectToDB()
        mycursor = cont.cursor()
        mycursor.execute(
            "SELECT * FROM office WHERE id = '" + self.id + "' or name = '" + self.name + "'")
        myresult = mycursor.fetchall()
        return myresult

    # UPDATE OFFICE METHOD (U => CRUD)
    def update_office(self):
        # update office
        cont = connectToDB()
        mycursor = cont.cursor()
        mycursor.execute(
            "UPDATE office SET name = '" + self.name + "' WHERE id = '" + self.id + "'")
        cont.commit()
        return 'office updated'

    # REMOVES OFFICE METHOD (D => CRUD)
    # @classmethod
    def remove_office(self):
        if( checkInt(self.id) and self.id > 0):
            if(self.checkOffice()):
                cont = connectToDB()
                mycursor = cont.cursor()
                mycursor.execute(
                    "DELETE FROM office WHERE id = " + str(self.id) + " or name = '" + self.name + "'")
                cont.commit()
                return 'office removed'
            else:
                return 'office not found'
        else:
            return 'office id must be greater than 0'
        
    ## CHECKS IF OFFICE EXISTS
    def check_office(self):
        # check office
        cont = connectToDB()
        mycursor = cont.cursor()
        mycursor.execute(
            "SELECT * FROM office WHERE id = '" + self.id + "' or name = '" + self.name + "'")
        myresult = mycursor.fetchall()
        if(myresult):
            return False
        else:
            return True

    ## CHECKS IF EMPLOYEE EXISTS
    def check_employee(self, id):
        # check employee
        cont = connectToDB()
        mycursor = cont.cursor()
        mycursor.execute(
            "SELECT * FROM employee WHERE id = '" + str(self.id) + "'")
        myresult = mycursor.fetchall()
        if(myresult):
            return True
        else:
            return False

    ## GETS ALL Offices
    # @classmethod
    def get_all_offices():
        con = connectToDB()
        mycursor = con.cursor()

        mycursor.execute("SELECT * FROM office")
        myresult = mycursor.fetchall()
        return myresult

    ## GETS A SINGLE EMPLOYEE
    # @classmethod
    def get_employee_by_id(self, id):
        self.id = id
        if(checkInt(id) and self.check_employee(id)):
            conn = connectToDB()
            mycursor = conn.cursor()

            mycursor.execute("SELECT * FROM employee WHERE id = " + str(self.id))
            myresult = mycursor.fetchall()
            return myresult
        else:
            return 'employee not found'

    ## HIRES AN EMPLOYEE
    # @classmethod
    def hire_employee(self, employee):
        conn = connectToDB()
        mycursor = conn.cursor()

        mycursor.execute("INSERT INTO employee(email, workmood, salary, is_manager, office_id) VALUES ('" + employee.email + "','" + employee.workmood + "','" + str(employee.salary) + "','" + str(employee.is_manager) + "','" + str(employee.office_id) + "')")
        conn.commit()
        return 'employee hired'

    ## FIRES AN EMPLOYEE
    @staticmethod
    def fire_employee(id):
        conn = connectToDB()
        mycursor = conn.cursor()

        mycursor.execute("DELETE FROM employee WHERE id = " + str(id))
        conn.commit()
        return 'employee fired'

    ## CHECKS IF OFFICE EXISTS
    @staticmethod
    def check_office_static(id):
        if(checkInt(id)):
            # check office
            cont = connectToDB()
            mycursor = cont.cursor()
            mycursor.execute(
                "SELECT * FROM office WHERE id = '" + id + "'")
            myresult = mycursor.fetchall()
            if(myresult):
                return True
        return False

    @staticmethod
    def check_office_static_Name(name):
        if(checkString(name)):
            # check office
            cont = connectToDB()
            mycursor = cont.cursor()
            mycursor.execute(
                "SELECT * FROM office WHERE name = '" + name + "'")
            myresult = mycursor.fetchall()
            if(myresult):
                return True
        return False
    
    # @classmethod
    def get_all_employees(self):
        # return all offices
        cont = connectToDB()
        mycursor = cont.cursor()
        mycursor.execute("SELECT * FROM employee where office_id = " + str(self.office_id))
        myresult = mycursor.fetchall()
        return myresult


# ##############################################################################


def check_office_name(name):
    # check if office name is unique
    cont = connectToDB()
    mycursor = cont.cursor()
    mycursor.execute(
        "SELECT * FROM office WHERE name = '" + name + "'")
    myresult = mycursor.fetchall()
    if(myresult):
        return False
    else:
        return True

def check_Employee():
    emp_id = input("Enter Employee Id : ")
    cont = connectToDB()
    mycursor = cont.cursor()
    mycursor.execute(
        "SELECT * FROM employee WHERE id = " + str(emp_id))
    myresult = mycursor.fetchall()
    if(len(myresult) == 0):
        return False
    else:
        return True

def check_EmployeeWithID(emp_id):
    cont = connectToDB()
    mycursor = cont.cursor()
    mycursor.execute(
        "SELECT * FROM employee WHERE id = " + str(emp_id))
    myresult = mycursor.fetchall()
    if(len(myresult) == 0):
        return False
    else:
        return True

###############################################################################
# new employee

def check_office_exist(id):
    # check if office id is unique
    cont = connectToDB()
    mycursor = cont.cursor()
    mycursor.execute(
        "SELECT * FROM office WHERE id = '" + id + "'")
    myresult = mycursor.fetchall()
    if(myresult):
        return True
    else:
        return False  

def new_employee():

    # if(check_Employee()):
    #     print('Employee already exists')
    #     return
    # else:

    email = input("Enter Employee Email : ")
    if(check(email)) == False:
        print('invalid email')
        return
    workmood = input("Enter Employee Workmood : ")

    salary = input("Enter Employee Salary : ")
    if(checkInt(salary)) == False:
        print('invalid salary')
        return
    elif(int(salary) < 1000):
        print('salary is too low, it must be 1000 or more')
        return

    is_manager = input("Is Manager? (y/n) : ")
    if(is_manager == 'y'):
        is_manager = True
    elif(is_manager == 'n'):
        is_manager = False
    else:
        print('invalid input')
        return

    office_id = input("Enter Employee Office Id : ")

    if not (Office.check_office_static(office_id)):
        print('office not found')
        return

    # office_name = input("Enter Employee Office Name : ")
    # if not (Office.check_office_static_Name(office_name)):
    #     print('office not found')
    #     return

    employee = Employee(email, workmood, int(salary), is_manager, office_id)
    office = Office(office_id)
    office.hire_employee(employee)
    # employee.add_employee()
    print('Employee added')

def new_office():
    name = input("Enter Office Name : ")
    if(Office.check_office_static_Name(name) == True):
        print('Office Name was already taken')
        return
    office = Office(1)
    office.add_office(name)
    print('Office added')

def delete_Employee():
    emp_id = input("Enter Employee Id : ")
    if(check_EmployeeWithID(emp_id)):
        Office.fire_employee(emp_id)
        print('Employee deleted')
    else:
        print('Employee does not exist')

def display_all_employees():
    office_id = input("Enter Office Id : ")
    if not (checkInt(office_id)):
        print('Office Id is not valid')
        return
    if not (Office.check_office_static(office_id)):
        print('Office Id is not valid')
        return

    office = Office(office_id)
    emps = office.get_all_employees()
    print(':::::::: Employees in Office ' + office_id + ' :::::::: ')
    for emp in emps:
        print("Employee Id : ", emp[0])
        print("Employee Email : ", emp[1])
        print("Employee WorkMood : ", emp[2])
        if(emp[4] == 1):
            print("Employee Salary : Employee is Manager, You can't view his/her salary")
        else:
            print("Employee Salary : ", emp[3])

        print("Employee Status(Manager) : ", bool(emp[4]))
        print("Employee Office ID : ", emp[5])
        print("Employee Reg Date: ", emp[6])
    print('------------------------------------')

def display_all_offices():
    eksde = Office.get_all_offices()
    print('::::::::' + ' All Offices ' + ' :::::::: ')
    print(eksde)
    for i in eksde:
        print("Office Id : ", i[0])
        print("Office Name : ", i[1])
    print('------------------------------------')

def display_specific_employee():
    emp_id = input("Enter Employee Id : ")
    if(check_EmployeeWithID(emp_id)):
        office = Office(1)
        eksde = office.get_employee_by_id(emp_id)
        print('::::::::' + ' Employee ' + emp_id + ' :::::::: ')
        print("Employee Id : ", eksde[0][0])
        print("Employee Email : ", eksde[0][1])
        print("Employee WorkMood : ", eksde[0][2])
        if(eksde[0][4] == 1):
            print("Employee Salary : Employee is Manager, You can't view his/her salary")
        else:
            print("Employee Salary : ", eksde[0][3])

        print("Employee Status(Manager) : ", bool(eksde[0][4]))
        print("Employee Office ID : ", eksde[0][5])
        print("Employee Reg Date: ", eksde[0][6])
        print('------------------------------------')
    else:
        print('Employee does not exist')

def print_menu():
    print("Enter your Choice ")
    print("1 to Add Employee")
    print("2 to Add Office ")
    print("3 to Fire Employee")
    print("4 to Display All Employees")
    print("5 to Display All Offices")
    print("6 to Display Specific Employee")
    print("q to Exit")

def menu():
    print("Welcome to Employee Management System")
    print_menu()
    # Taking choice from user
    ch = input("Enter your Choice:  ")
    while(ch != 'q'):
        os.system('cls')
        if(ch == '1'):
            new_employee()
        elif(ch == '2'):
            new_office()
        elif(ch == '3'):
            delete_Employee()
        elif(ch == '4'):
            display_all_employees()
        elif(ch == '5'):
            display_all_offices()
        elif(ch == '6'):
            display_specific_employee()
        else:
            print("Invalid Choice")
        print_menu()
        ch = input("Enter your Choice ")

menu()