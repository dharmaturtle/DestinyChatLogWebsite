import datetime, math, psycopg2
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from logapp.models import Log, Log_wordcount, Log_wordline_count, Log_populartimes, Log_emote, Log_popularity, Log_network_summary, Log_streams, Log_wordline_count_meta, Log_wordline_std_meta
from pymongo import MongoClient
from collections import OrderedDict

def default_view(request, type = "", log_list = "", q = ""):
	if not log_list and not type:
		log_list = Log.objects.filter().order_by("-time")
	
	paginator = Paginator(log_list, 30)   # Show 30 per page
	page = request.GET.get('page')
	
	try:
		log_list = paginator.page(page)
	except (PageNotAnInteger, TypeError): # If page is not an integer or doesn't exist, deliver first page.
		log_list = paginator.page(1)
	except EmptyPage:                     # If page is out of range (e.g. 9999), deliver last page of results.
		log_list = paginator.page(paginator.num_pages)
	
	if not q:
		return render_to_response('base_log.html', {"log_list": log_list, 'type': type})
	else:
		return render_to_response('base_log.html', {"log_list": log_list, 'type': type, 'query': q, })

def robots(request):
	return render_to_response('robots.txt')

def text_search(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		log_list = Log.objects.filter(text__icontains=q).order_by("-time")
		return default_view(request, "text", log_list, q)
	else:
		return default_view(request, "text")

def user_search(request):
	if 'q' in request.GET and request.GET['q']:
		q = request.GET['q']
		log_list = Log.objects.filter(user__icontains=q).order_by("-time")
		return default_view(request, "user", log_list, q)
	else:
		return default_view(request, "user")

def statistics(request):
	verbosity = Log_wordline_count.objects.filter().order_by("-linecount")[:50]
	verb_meta = Log_wordline_count_meta.objects.filter()[0]
	std = Log_wordline_std_meta.objects.filter()[0]
	
	#for property, value in vars(std).iteritems():
	#	print property, ": ", value
	
	total_average = verb_meta.totalword / verb_meta.totalline
	summation = 0
	for x in verbosity:
		summation += math.pow((x.wordcount / x.linecount - total_average),2)
	std_wl = math.sqrt(summation / verb_meta.totalline)
	
	summation = 0
	average_lines = verb_meta.totalline / len(verbosity)
	for x in verbosity:
		summation += math.pow((x.linecount - average_lines),2)
	std_lines = math.sqrt(summation / len(verbosity))
	
	wordcount = Log_wordcount.objects.filter().order_by("-value")[:50]
	popularity = Log_popularity.objects.filter().order_by("-value")[:50]
	populartimes = Log_populartimes.objects.filter().order_by("hour")
	emote = Log_emote.objects.filter().order_by("-value")
	network = Log_network_summary.objects.filter().order_by("-sumvalue")[:50]
	
	populartimesjson = '['
	i = 0
	for x in populartimes:
		populartimesjson += str(x.value) + ", "
	populartimesjson = populartimesjson[:-1]
	populartimesjson += ']'
	#print populartimesjson
	
	emotejson = '['
	i = 1
	for x in emote:
		emotejson += '{"value":' + str(x.value) + ', "name":"' + x.face + '", "ordinal":' + str(i) + '},'
		i += 1
	emotejson = emotejson[:-1]
	emotejson += ']'
	#print emotejson
	
	wordcountjson = '['
	i = 1
	for x in wordcount:
		wordcountjson += '{"value":' + str(x.value) + ', "name":"' + x.word + '", "ordinal":' + str(i) + '},'
		i += 1
	wordcountjson = wordcountjson[:-1]
	wordcountjson += ']'
	#print wordcountjson
	
	verbosityjson = '['
	i = 1
	for x in verbosity:
		verbosityjson += '{"value":' + str(x.linecount) + ', "wordcount":' + str(x.wordcount) + ', "name":"' + x.user + '", "ordinal":' + str(i) + '},'
		i += 1
	verbosityjson = verbosityjson[:-1]
	verbosityjson += ']'
	#print verbosityjson
	
	popularityjson = '['
	i = 1
	for x in popularity:
		popularityjson += '{"value":' + str(x.value) + ', "name":"' + x.user + '", "ordinal":' + str(i) + '},'
		i += 1
	popularityjson = popularityjson[:-1]
	popularityjson += ']'
	#print popularityjson
	
	
	return render_to_response('base_statistics.html', {"verbosity": verbosityjson, "wordcount": wordcountjson, 'type': 'statistics', 'populartimes':populartimesjson, 'emote':emotejson, 'popularity':popularityjson, 'network':network, 'verb_meta':verb_meta, 'std_wl':std_wl, 'std_lines':std_lines, 'total_average':total_average, 'average_lines':average_lines, 'std':std},)

def chronological(request):
	now = datetime.datetime.now()
	dt=list(now.timetuple())
	default = False
	
	if 'q' in request.GET and request.GET['q']:
		try:
			y = int(request.GET['y'])
			m = int(request.GET['m'])
			d = int(request.GET['d'])
			h = int(request.GET['h'])
			min = int(request.GET['min'])
			left  = "?q=search&y=" + str(y) + "&m=" + str(m) + "&d=" + str(d) + "&h=" + str(h) + "&min=" + str((min + 1))
			right = "?q=search&y=" + str(y) + "&m=" + str(m) + "&d=" + str(d) + "&h=" + str(h) + "&min=" + str((min - 1))
			log_list = Log.objects.filter(time__range=(datetime.datetime(y, m, d, h, min), datetime.datetime(y, m, d, h, min + 1))).order_by("-time")
			return render_to_response('base_chronological.html', {'log_list': log_list, 'type': 'chronological', 'time': datetime.datetime(y, m, d, h, min), 'y':y, 'm':m, 'd':d, 'h':h, 'min':min, 'right': right, 'left': left})
		except: #todo: Display error screen
			print "User manually input invalid value (probably)"
	log_list = Log.objects.filter(time__range=(datetime.datetime(dt[0], dt[1], dt[2], dt[3], dt[4]), now)).order_by("-time")
	right = "?q=search&y=" + str(dt[0]) + "&m=" + str(dt[1]) + "&d=" + str(dt[2]) + "&h=" + str(dt[3]) + "&min=" + str(dt[4] - 1)
	return render_to_response('base_chronological.html', {'log_list': log_list, 'type': 'chronological', 'time': now, 'right': right})

def streams(request):
	streams = Log_streams.objects.filter().order_by("-time")[:3]
	
	streams_dict = {}
	for x in streams:
		for y in x.streams:
			if y.name not in streams_dict:
				streams_dict[y.name] = []
			streams_dict[y.name].append([x.time, y.viewers])
			#break #uncomment to test just 1 person
	#for x in streams_dict:
	#	#print "var " + x + " = " + str(streams_dict[x]).replace("datetime.datetime", "new Date") + ";"
	#	print "var " + x + " = " + str(streams_dict[x]).replace("datetime.datetime", "Date.UTC") + ";"
	
	#var d2 = [[0, 3], [4, 8], [8, 5], [9, 13]];
	#var qq = [[Date.UTC(2011, 2, 12, 14, 0, 0), 28],[Date.UTC(2011, 2, 12, 15, 0, 0), 27],[Date.UTC(2011, 2, 12, 16, 0, 0), 25],];
	#var TSM_TheOddOne = [[new Date(2013, 10, 28, 21, 20, 30), 23958], [datetime.datetime(2013, 10, 28, 21, 17, 30), 25035], [datetime.datetime(2013, 10, 28, 21, 14, 30), 24755]];
	
	return render_to_response('base_streams.html', {'streams_dict':streams_dict, 'type': 'streams'})

def streamsdata(request):
	client = MongoClient('mongodb://localhost:27017/')
	total = client['testDB2']['logapp_log_streams'].find({"time": {"$gt": datetime.datetime.now() - datetime.timedelta(minutes=720)}}).sort('time')
	records = OrderedDict((record['_id'], record) for record in total)

	streamers = []

	for x in records:
		for y in records[x]['streams'][:5]:
			#print str(records[x]['time']) + " " + y['name'] + " " + str(y['viewers'])
			if y['name'] not in streamers:
				streamers.append(y['name'])

	output = "date\t"
	for i, x in enumerate(streamers):
		if ((i+1) != len(streamers)):
			output += x + "\t"
		else:
			output += x
	output += "\n"

	for x in records:
		output += str(records[x]['time']) + "\t"
		for i, z in enumerate(streamers):
			for y in records[x]['streams'][:5]:
				if z == y['name']:
					viewers = str(y['viewers'])
					break
			if ((i+1) != len(streamers)):
				output += viewers + "\t"
			else:
				output += viewers
			viewers = "null"
		output += "\n"
	return render_to_response('data.html', {'output':output})

def time(request):
	return render_to_response('data.html', {'output':datetime.datetime.now()})

def sql(request):
	try:
		page = int(request.GET.get('page'))
	except:
		page = 0
	if page < 0:
		page = 0
	offset = page * 30
	
	conn = psycopg2.connect("dbname='' user='' host='' password=''")
	cur = conn.cursor()
	cur.execute("SELECT * FROM logs_text ORDER BY -number LIMIT 30 OFFSET " + str(offset) + ";") #technically shouldn't do this, but I know its an int, so no injection
	
	log_list = []
	for x in cur.fetchall():
		log_dict = {}
		log_dict['index'] = x[0]
		log_dict['text'] = x[1]
		log_dict['time'] = x[2]
		log_dict['user'] = x[3]
		log_list.append(log_dict)
	
	return render_to_response('base_sql.html', {'log_list':log_list, 'page':page, 'type': 'sql'})