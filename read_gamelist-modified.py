#!/usr/bin/python
import psycopg2
"""
A Program for reading a dat file into a postgresql database
"""

db_username = "postgres"
db_password = ""
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
#                 "<video>", "<marquee>", "<thumbnail>", "<developer>",
#                 "<publisher>", "<genre>", "players"]
tag_list = ["<path>", "<name>", "<sortname>", "<image>", "<video>",
            "<marquee>", "<thumbnail>", "<rating>", "<releasedate>",
            "<developer>", "<publisher>", "<genre>", "<players>",
            "<region>", "<favorite>", "<hidden>", "<kidgame>",
            "<playcount>", "<lastplayed>"]
#tag_list_number = ["<rating>", "<releasedate>", "<favorite>",
#                   "<hidden>", "<kidgame>", "<playcount>",
#                   "<lastplayed>"]
#row_numbers = ["game_id", "rating", "playcount"]
#row_text    = ["path", "name", "sortname", "image", "video", "marquee",
#               "thumbnail", "releasedate", "developer", "publisher",
#               "genre", "players", "region", "lastplayed"]
row_boolean = ["favorite", "hidden", "kidgame"]
insert_rows = ''
insert_values = ''
system_id = 5
gamelist = open("gamelist.xml","r")
#sqlfile = open("sql.txt","w")
game_info = {}

#insert_rows = "INSERT INTO gamelist_test (system_id"
#insert_values = "VALUES (%d, ", (system_id)


for line in gamelist:
    game_id = 0
    source = ""
    path = ""
    name = ""
    sortname = ""
    image = ""
    video = ""
    marquee = ""
    thumbnail = ""
    rating = 0.0
    releasedate = ""
    developer = ""
    publisher = ""
    genre = ""
    players = ""
    region = ""
    favorite = ""
    hidden = ""
    kidgame = ""
    playcount = ""
    lastplayed = ""

    if ('<game id' in line):
        tag = '<game id="'
        game_id = line[line.index(tag) + len(tag):line.index('" source')]
        #insert_rows = insert_rows + ", game_id"
        #insert_values = insert_values + ", %s " + 
        #game_info.update({'game_id':line[line.index(tag) + len(tag):line.index('" source')]})
        tag = 'source="'
        source = line[line.index(tag) + len(tag):line.index('">')]
        #game_info.update({'source':line[line.index(tag) + len(tag):line.index('">')]})

    tag = '<path>'
    if (tag in line):
        path = line[line.index(tag) + len(tag):line.index('</')]

    tag = '<name>'
    if (tag in line):
        name = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<sortname>'
    if (tag in line):
        sortname = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<image>'
    if (tag in line):
        image = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<video>'
    if (tag in line):
        video = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<marquee>'
    if (tag in line):
        marquee = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<thumbnail>'
    if (tag in line):
        thumbnail = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<rating>'
    if (tag in line):
        rating = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<releasedate>'
    if (tag in line):
        releasedate = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<developer>'
    if (tag in line):
        developer = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<publisher>'
    if (tag in line):
        publisher = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<genre>'
    if (tag in line):
        genre = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<players>'
    if (tag in line):
        players = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<region>'
    if (tag in line):
        region = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<favorite>'
    if (tag in line):
        favorite = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<hidden>'
    if (tag in line):
        hidden = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<kidgame>'
    if (tag in line):
        kidgame = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<playcount>'
    if (tag in line):
        playcount = line[line.index(tag) + len(tag):line.index('</')]

    tag ='<lastplayed>'
    if (tag in line):
        lastplayed = line[line.index(tag) + len(tag):line.index('</')]








#    for tag in tag_list:
#        if (tag in line):
#            data_start = line.index(tag)+ len(tag)
#            data_end = line.index("</")
#            game_info.update({tag[1:-1]:line[data_start:data_end]})

#    for tag in tag_list_number:
#        if (tag in line):
#            data_start = line.index(tag)+ len(tag)
#            data_end = line.index("</")
#             game_info.update({tag[1:-1]:line[data_start:data_end]})

    if ("</game>" in line):

        sql = "INSERT INTO gamelist (system_id, game_id, source, path, name, sortname, image, video, marquee, thumbnail, rating, releasedate, developer, publisher, genre, players, region, favorite, hidden, kidgame, playcount, lastplayed) VALUES (%d, %d, %s, %s, %s, %s, %s, %s, %s, %s, %f, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        print (sql, (system_id, game_id, source, path, name, sortname, image, video, marquee, thumbnail, rating, releasedate, developer, publisher, genre, players, region, favorite, hidden, kidgame, playcount, lastplayed))
        cursor.execute(sql, (system_id, game_id, source, path, name, sortname, image, video, marquee, thumbnail, rating, releasedate, developer, publisher, genre, players, region, favorite, hidden, kidgame, playcount, lastplayed))



"""
        insert_rows = "INSERT INTO gamelist_test (system_id, "
        insert_values = "VALUES (" + system_id + ", "

        for key in game_info.keys():
            insert_rows = insert_rows + key + ", "
        insert_rows = insert_rows + ") "

        for value in game_info.values():
#            print (type(value))o
            insert_values = insert_values + "'''" + value + "''', "
        insert_values = insert_values + ")"

        insert_rows = insert_rows[:-4] + insert_rows[-2:]
        insert_values = insert_values[:-4] + insert_values[-1:]

        gamelist_insert = insert_rows + insert_values + ";"
        sqlfile.write(gamelist_insert)
        sqlfile.close()
        print (gamelist_insert)
        cursor.execute(gamelist_insert)
"""


gamelist.close()
if(connection):
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")
