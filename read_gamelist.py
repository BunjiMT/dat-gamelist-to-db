#!/usr/bin/python
import psycopg2
"""
A Program for reading a dat file into a postgresql database
"""

db_username = "postgres"
db_password = "****"
db_hostname = "wdb-serv"
db_database = "arcade"
db_port     = 5432

try:
	connection = psycopg2.connect(user = db_username,
									password = db_password,
									host = db_hostname,
									port = db_port,
									database = db_database)


	cursor = connection.cursor()
	# Print PostgreSQL Connection properties
	#print ( connection.get_dsn_parameters(),"\n")

	# Print PostgreSQL version
	#cursor.execute("SELECT version();")
	#record = cursor.fetchone()
	#print("You are connected to - ", record,"\n")

except (Exception, psycopg2.Error) as error :
	print ("Error while connecting to PostgreSQL", error)
#finally:
	#closing database connection.


tag = ""
#tag_list_text = ["<path>", "<name>", "<sortname>", "<desc>", "<image>",
#                  "<video>", "<marquee>", "<thumbnail>", "<developer>",
#                  "<publisher>", "<genre>", "players"]
tag_list = ["<path>", "<name>", "<sortname>", "<image>", "<video>",
			"<marquee>", "<thumbnail>", "<rating>", "<releasedate>",
			"<developer>", "<publisher>", "<genre>", "<players>",
			"<region>", "<favorite>", "<hidden>", "<kidgame>",
			"<playcount>", "<lastplayed>"]
#tag_list_number = ["<rating>", "<releasedate>", "<favorite>",
#                   "<hidden>", "<kidgame>", "<playcount>",
#                   "<lastplayed>"]
row_number = ["game_id", "rating", "playcount"]
insert_rows = ''
insert_values = ''
system_id = '5'
gamelist = open("gamelist.xml","r")
game_info = {}

for line in gamelist:

	if ('<game id' in line):
		tag = '<game id="'
		game_info.update({'game_id':line[line.index(tag) + len(tag):line.index('" source')]})
		tag = 'source="'
		game_info.update({'source':line[line.index(tag) + len(tag):line.index('">')]})

	for tag in tag_list:
		if (tag in line):
			data_start = line.index(tag)+ len(tag)
			data_end = line.index("</")
			game_info.update({tag[1:-1]:line[data_start:data_end]})

#   for tag in tag_list_number:
#       if (tag in line):
#           data_start = line.index(tag)+ len(tag)
#           data_end = line.index("</")
#           game_info.update({tag[1:-1]:line[data_start:data_end]})

	if ("</game>" in line):
		insert_rows = 'INSERT INTO gamelist_test (system_id, '
		insert_values = 'VALUES (' + system_id + ',"'

		for key in game_info.keys():
			insert_rows = insert_rows + key + ', '
		insert_rows = insert_rows + ') '

		for value in game_info.values():
#           print (type(value))
			insert_values = insert_values + value + '", "'
		insert_values = insert_values + ')'

		insert_rows = insert_rows[:-4] + insert_rows[-2:]
		insert_values = insert_values[:-4] + insert_values[-1:]

		gamelist_insert = insert_rows + insert_values
		print (gamelist_insert)
		cursor.execute(gamelist_insert + ';')



gamelist.close()
if(connection):
	cursor.close()
	connection.close()
	print("PostgreSQL connection is closed")
