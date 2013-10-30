# Logs chat to a PostgreSQL DB

import psycopg2
import sys, traceback
import json
import datetime
import time
import select
from websocket import create_connection
from colorama import init, Fore, Back, Style
init()
mydict = {"\u003e":">","\u003c":"<","\\\"":"\"","\\\\":"\\"} #escaping/unescaping chars

conn = psycopg2.connect("dbname='' user='' host='' password=''")
cur = conn.cursor()
print 'Connected...'

def log(c,s):
	print(Fore.BLUE + Style.BRIGHT + time.asctime() + Fore.RESET + " " + c + s + Fore.RESET + Back.RESET + Style.NORMAL)
def mlog(user,message):
	print(Fore.BLUE + Style.BRIGHT + time.asctime() + " " + Fore.GREEN + user + " " + Fore.RESET + " " + message + Fore.RESET + Back.RESET + Style.NORMAL)
	query = "INSERT INTO logs_text (username, text ) VALUES (%s, %s );" #user is a reserved word :(
	data = (user,message)	# proper way to pass http://www.psycopg.org/psycopg/docs/usage.html#passing-parameters-to-sql-queries
	cur.execute(query, data)
	conn.commit()			# Todo: Cache the data, so we don't commit on every line.
def wsconnect():
	global ws
	ws = create_connection("ws://www.destiny.gg:9998/ws", header={"Origin: http://www.destiny.gg"})
	log(Fore.GREEN , "ws connect")
wsconnect()
log(Fore.BLUE + Back.RED , "v117.beta" ) #microversioning number
while 1:
	try:
		(r, w, x) = select.select([ws], [], [])
		for sock in r:
			try:
				ggtime = datetime.datetime.utcnow()
				data = sock.recv().strip('\r\n')
				if data[:3] == "ERR":
					if sock == ws:
						socky = "ws"
					else:
						socky = "unknown sock"
					mlog("SERVER_MESSAGE", socky + ":" + data)
				if data[0:4] == "PING":
					sock.send("PONG" + data[4:])
				if sock == ws:
					a = data.split(' ',1)
					command = a[0]
					try:
						payload = json.loads(a[1])
					except (KeyboardInterrupt, SystemExit):
						raise
					except:
						mlog("SERVER_MESSAGE", "JSON error: Probable disconnect. " + data)
						log(Fore.RED, "Json error: " + data )
					if command == "MSG":
						mystr = payload["data"]
						for k, v in mydict.iteritems():
							mystr = mystr.replace(k, v)
						mlog(payload["nick"],mystr)
					elif command == "MUTE":
						mlog(payload["nick"]," <=== just muted " + payload["data"])
					elif command == "UNMUTE":
						mlog(payload["nick"]," <=== just unmuted " + payload["data"])
					elif command == "SUBONLY":
						if payload["data"] == "on":
							mlog(payload["nick"], " <=== just enabled subscribers only mode.")
						else:
							mlog(payload["nick"], " <=== just disabled subscribers only mode.")
					elif command == "BAN":
						mlog(payload["nick"], " <=== just banned " + payload["data"])
					elif command == "UNBAN":
						mlog(payload["nick"], " <=== just unbanned " + payload["data"])
					elif command == "PING":
						sock.send("PONG" + data[4:])
					elif command == "NAMES" or command == "QUIT" or command == "JOIN":
						pass
					elif command != "":
						mlog("SERVER_MESSAGE", data)
			except:
				try:
					time.sleep( 2 )		# gives time for server to recover
					if sock == ws:
						mlog("SERVER_MESSAGE","Websocket disconnect, attempting reconnect...")
						wsconnect()
				except (KeyboardInterrupt, SystemExit):
					raise
				except:
					log(Fore.RED,"Random error in dharmagg?")
			if int((datetime.datetime.utcnow() - ggtime).total_seconds()) > 120:
				wsconnect()
			#print data
	except (KeyboardInterrupt, SystemExit):
		raise
	except:
		try:
			log(Fore.RED , "penultimate error " + str(data))
			traceback.print_tb(sys.exc_info()[2])
			log(Fore.RED , str(sys.exc_info()))
		except:
			log(Fore.RED , "horrible error")