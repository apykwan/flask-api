from server import db, app
# import mysql.connector


# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="taipei"
# )

# my_cursor = mydb.cursor()
# my_cursor.execute("CREATE DATABASE IF NOT EXISTS users")
# my_cursor.execute("SHOW DATABASES")
# for db in my_cursor:
#   print(db)


with app.app_context():
  db.create_all()