from dataBase import *


class Person:
    healthRate = 0

    def __init__(self, full_name, money, sleepmood, healthRate):
        self.full_name = full_name
        self.money = money
        self.sleepmood = sleepmood
        self.healthRate = healthRate

    # sleep method
    def sleep(self, hours):
        if hours == 7:
            self.sleepmood = 'happy'
            print('your sleepmood changed to happy')
        elif hours > 7:
            self.sleepmood = 'lazy'
            print('your sleepmood changed to lazy')
        elif hours < 7:
            self.sleepmood = 'tired'
            print('your sleepmood changed to tired')
            return self.sleepmood
        else:
            return 'please enter values in range'

    def sethealthRate(self, healthRate):
        if healthRate >= 0 and healthRate <= 100:
            self.healthRate = healthRate
        else:
            print('out of range')

    # eat method
    def eat(self, meals):
        if meals <= 3 and meals >= 1:
            if meals == 3:
                self.healthRate = '100'
                print('your healthRate changed to 100')
            elif meals == 2:
                self.healthRate = '75'
                print('your healthRate changed to 75')
            elif meals == 1:
                self.healthRate = '50'
                print('your healthRate changed to 50')
            return self.healthRate
        else:
            print('out of range')

    def buy(self, items):
        if items == 1:
            self.money -= 10
            print('Your money decreased by 10')


class Employee(Person):

    def __init__(self, email, workmood, salary, is_manager):
        self.email = email
        self.workmood = workmood
        self.salary = salary
        self.is_manager = is_manager

    def sendEmail(self, to, subject, body, receiver_name):
        f = open('email.txt', 'w')
        f.write(f'email is sent to : {to} \n')
        f.write(f'email subject is :{subject} \n')
        f.write(f'email body is :{body} \n')
        f.write(f'email sender is : {receiver_name} \n')
        f.close()

    def work(self, hours):
        if hours == 8:
            self.workmood = 'happy'
            print('your workmood changed to happy')
        elif hours < 8:
            self.workmood = 'lazy'
            print('your workmood changed to lazy')
        elif hours > 8:
            self.workmood = 'tired'
            print('your workmood changed to tired')
        return self.workmood

    @classmethod
    def fire_employee(cls, id):
        # fire employee by id
        cont = mysqlconnect()
        mycursor = cont.cursor()
        mycursor.execute(
            "DELETE FROM employee WHERE id = " + str(id))
        cont.commit()
        return 'employee fired'


class Office():

    def __init__(self, name):
        self.name = name

    def get_all_employees():
        # return all employees
        cont = mysqlconnect()
        mycursor = cont.cursor()
        mycursor.execute("SELECT * FROM employee")
        myresult = mycursor.fetchall()
        return myresult

    @classmethod
    def get_employee(cls, id):
        # get employee by id
        cont = mysqlconnect()
        mycursor = cont.cursor()
        mycursor.execute(
            "SELECT * FROM employee WHERE id = " + str(id))
        myresult = mycursor.fetchall()
        return myresult

    def hire(self, employee):
        print(employee.email)

        cont = mysqlconnect()
        mycursor = cont.cursor()
        mycursor.execute(
            "INSERT INTO employee(email, workmood, salary, is_manager, office_id) VALUES ('" + employee.email + "','" + employee.workmood + "','" + str(employee.salary) + "','" + str(employee.is_manager) + "','" + "1" + "')")
        cont.commit()
        cont.close()
        return 'employee hired'

    def add_office(self):
        # add office
        cont = mysqlconnect()
        mycursor = cont.cursor()
        mycursor.execute(
            "INSERT INTO office(name) VALUES('" + self.name + "')")
        cont.commit
        return 'office added'
