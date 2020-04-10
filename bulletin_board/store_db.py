import mysql.connector as mysql


class checkDB():
	def __init__(self):
		pass

	def check_db(self):
		db = mysql.connect(
	    	host = "localhost",
	    	user = "root",
	    	passwd = "Nowayyoucan"
		)

		cursor = db.cursor()
		cursor.execute("SHOW DATABASES")
		databases = cursor.fetchall()

		if ('bulletin_board',) in databases:
			print("Database Exists!")
		else:
			cursor.execute("CREATE DATABASE bulletin_board")
		
		cursor.execute("USE bulletin_board")

		return db