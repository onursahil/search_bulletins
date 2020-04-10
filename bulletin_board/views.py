from django.shortcuts import render
from .models import Post
from django.shortcuts import redirect
from bulletin_board.crawling_get_worldJob import *
from bulletin_board.crawling_get_kosaf import *
from bulletin_board.crawling_get_youthcenter import *
from bulletin_board.store_db import *
from bulletin_board.db_table import *
from bulletin_board.db_data_check import *
import datetime

# Create your views here.

def home(request):
	return render(request, 'bulletin_board/home.html')

def results(request):
	search_q = request.GET.get('search')
	search_query = []
	search_keyword = {
		'keyword': search_q
	}
	search_query.append(search_keyword)
	bulletin_list = get_crawling_results(search_q)
	print("\n")
	print("BULLETIN LIST")
	print(bulletin_list)

	db = db_process()
	db = db_table_process(db)
	today = datetime.datetime.today()
	compare_and_insert(db, bulletin_list, today)

	cursor = db.cursor()
	cursor.execute("SELECT * FROM bulletins")
	all_current_data = cursor.fetchall()

	print("\n")
	display_data = []
	for i in range(len(all_current_data)):
		temp_dict = {}
		temp_dict['post_date'] = all_current_data[i][0]
		temp_dict['crawled_date'] = all_current_data[i][1]
		temp_dict['title'] = all_current_data[i][2]
		temp_dict['link'] = all_current_data[i][3]
		display_data.append(temp_dict)

	print("ALL CURRENT DATA")
	print(display_data)

	context = {
		'posts': display_data,
		'search_q': search_query
	}

	return render(request, 'bulletin_board/results.html', context)

def get_crawling_results(keyword):
	worldJob = BWU_worldJob()
	kosaf = BWU_kosaf()
	youthcenter = BWU_youthcenter()

	count = 5

	results_worldJob = worldJob.get_notice(keyword, count)
	results_kosaf = kosaf.get_notice(keyword, count)
	results_youthcenter = youthcenter.get_notice(keyword, count)

	bulletin_list = (results_worldJob + results_kosaf + results_youthcenter)

	return bulletin_list

def db_process():
	db_check = checkDB()
	db = db_check.check_db()
	return db

def db_table_process(db):
	db_table = processTable()
	db = db_table.table_process(db)
	return db

def compare_and_insert(db, bulletin_list, today):
	db_data = checkData()
	db_data.data_check(db, bulletin_list, today)
