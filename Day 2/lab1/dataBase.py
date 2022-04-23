import MySQLdb


def mysqlconnect():
    try:
        con = MySQLdb.connect(
            "localhost", "root", "", "python")
    except:
        print("Unable to connect to database.")
        return 0
        
    cursor = con.cursor()
    return con


mysqlconnect()
