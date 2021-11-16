"""A one line summary of the module or program, terminated by a period.

Leave one blank line.  The rest of this docstring should contain an
overall description of the module or program.  Optionally, it may also
contain a brief description of exported classes and functions and/or usage
examples.
https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/

  Typical usage example:

  foo = ClassFoo()
  bar = foo.FunctionBar()
"""
# Module Imports
import mariadb
import sys

# Connect to MariaDB
try:
    conn = mariadb.connect(
        user="",
        password="",
        host="",
        port=3306,
        database="cryptotrend",
        autocommit=True         #automatically commits SQL statements

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

cur.execute(
    "SELECT * FROM test")

# Print Result-set
for line in cur:
    print(line)

try:
    cur.execute("INSERT INTO cryptotrend.test VALUES (10)")
except mariadb.Error as e:
    print(f"Error: {e}")
