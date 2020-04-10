# import mysql.connector as mysql

class processTable():
	def __init__(self):
		pass

	def table_process(self, db):
		cursor = db.cursor()
		cursor.execute("SHOW TABLES")
		tables = cursor.fetchall()
		print(tables)

		if ('bulletins',) in tables:
			print("Table Exists!")
		else:
			cursor.execute("CREATE TABLE  bulletins(post_date VARCHAR(255), crawled_date VARCHAR(255), title VARCHAR(255), link VARCHAR(255))")
			print('New Table Created!')

		return db