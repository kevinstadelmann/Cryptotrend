#https://www.kite.com/python/answers/how-to-execute-an-external-sql-file-using-sqlite3-in-python
# something like
#   sql = "INSERT INTO `employee` (`EmployeeID`, `Ename`, `DeptID`, `Salary`, `Dname`, `Dlocation`) VALUES (%s, %s, %s, %s, %s, %s)"
#     cursor.execute(sql, (1009,'Morgan',1,4000,'HR','Mumbai'))

# Module Imports
import mariadb
import sys
import sqlite3

# Connect to MariaDB
try:
    conn = mariadb.connect(
        user="root",
        password="123",
        host="127.0.0.1",
        port=3306,
        #database="test",
        autocommit=True         #automatically commits SQL statements

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

# load sql deployment
#var_sql_deployment = sql_file.read('sql_deployment.sql')
#cur.execute('sql_deployment.sql')

inputdir = 'deployment'

file_sql = open("sql_deployment.sql", "r")
var_sql = file_sql.read()
#print(var_sql)

#for line in fileinput.FileInput("file",inplace=1):
#    if line.rstrip():
#        print line

for statement in var_sql.split(';'):
    #exclude empty lines and comments
    if statement[0] not in ('#',' '):
        print(statement[0])
#with conn.cursor() as cur:
#cur.execute(statement)