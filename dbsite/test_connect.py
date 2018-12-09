import mysql.connector

mydb = mysql.connector.connect(
	host="sql9.freemysqlhosting.net",
	user="sql9265257",
	passwd="xGEis8B4An",
	database="sql9265257"
	
)


mycursor = mydb.cursor()

mycursor.execute("SHOW TABLES")

for x in mycursor:
	print(x)
	
	
mycursor.execute("SELECT * FROM location")

myresult = mycursor.fetchall()

for x in myresult:
	print(x)