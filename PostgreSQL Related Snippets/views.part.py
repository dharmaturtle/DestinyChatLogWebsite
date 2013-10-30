import datetime, math, psycopg2
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from logapp.models import Log, Log_wordcount, Log_wordline_count, Log_populartimes, Log_emote, Log_popularity, Log_network_summary, Log_streams, Log_wordline_count_meta, Log_wordline_std_meta

def sql(request):
	try:
		page = int(request.GET.get('page'))
	except:
		page = 0
	if page < 0:		# offset can't be negative
		page = 0
	offset = page * 30	# moving in blocks of 30
	
	conn = psycopg2.connect("dbname='' user='' host='' password=''")
	cur = conn.cursor()
	cur.execute("SELECT * FROM logs_text ORDER BY -number LIMIT 30 OFFSET " + str(offset) + ";") #technically shouldn't do this, but I know its an int, so no injection
	
	log_list = []		# making the output friendlier and keeps order
	for x in cur.fetchall():
		log_dict = {}
		log_dict['index'] = x[0]
		log_dict['text'] = x[1]
		log_dict['time'] = x[2]
		log_dict['user'] = x[3]
		log_list.append(log_dict)
	
	return render_to_response('base_sql.html', {'log_list':log_list, 'page':page, 'type': 'sql'})