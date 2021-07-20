import mysql.connector

mydb = mysql.connector.connect(host="umilitary.ml", user="max", passwd="maksikos973")

my_cursor = mydb.cursor()

#my_cursor.execute("CREATE TABLE if not exists max.my_shop")

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)

