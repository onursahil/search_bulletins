import datetime

class checkData():
	def __init__(self):
		pass

	def data_check(self, db, bulletin_list, today):
		cursor = db.cursor()
		cursor.execute("SELECT * FROM bulletins")
		result = cursor.fetchall()

		if len(result) == 0:
			cursor.executemany("""INSERT INTO bulletins (post_date, crawled_date, title, link) VALUES (%(post_date)s, %(crawled_date)s, %(title)s, %(link)s)""", bulletin_list)
			db.commit()
		else:
			cursor.execute("SELECT link FROM bulletins")
			db_link_data = cursor.fetchall()
			print('DB link data')
			print(db_link_data)

			cursor.execute('SELECT crawled_date FROM bulletins')
			db_crawleddate_data = cursor.fetchall()
			print('DB crawled date data')
			print(db_crawleddate_data)

			insert_to_db = []
			if today == datetime.datetime.strptime(db_crawleddate_data[0][0], "%Y.%m.%d"):
				for item in bulletin_list:
					if item['link'] not in db_link_data:
						insert_to_db.append(tuple(item))
				cursor.executemany("""INSERT INTO bulletins (post_date, crawled_date, title, link) VALUES (%(post_date)s, %(crawled_date)s, %(title)s, %(link)s)""", insert_to_db)
			else:
				cursor.execute("TRUNCATE bulletins")
				cursor.executemany("""INSERT INTO bulletins (post_date, crawled_date, title, link) VALUES (%(post_date)s, %(crawled_date)s, %(title)s, %(link)s)""", bulletin_list)
				db.commit()

			