#!/usr/bin/python
"""
A Program for reading a dat file into a postgresql database
"""

out_line = ""				#Output for printing info
add_mode = "FALSE"
tag = ""
section = ""
header_info = {}
header_tag_list = ["<name>", "<description>", "<version>", "<date>", "<author>", "<homepage>", "<url>"]
zip_tag_list = []
rom_tag_list = []
game_insert_rows = ''
game_insert_values = ''
system_id = '4'
header_id = 0
game_id = 0
dat_file = open("SegaCD.dat","r")

for line in dat_file:

	if ("<header>" in line):
		section = "header"

	if (section == "header"):
		for tag in header_tag_list:
			if (tag in line):
				data_start = line.index(tag)+ len(tag)
				data_end = line.index("</")
				header_info.update({tag[1:-1]:line[data_start:data_end]})

	if ("</header>" in line):
		section = ""
		insert_rows = "INSERT INTO no-intro_header (system_id, "
		insert_values = "VALUES (" + system_id + ",'"
		
		for key in header_info.keys():
			insert_rows = insert_rows + key + ", "
		insert_rows = insert_rows + ") "
		
		for value in header_info.values():
			insert_values = insert_values + value + "', '"
		insert_values = insert_values + ")"

		insert_rows = insert_rows[:-4] + insert_rows[-2:]
		insert_values = insert_values[:-4] + insert_values[-1:]
		
		header_insert = insert_rows + insert_values
		
		#header_id = "SELECT id FROM no-intro_header WHERE name = '" + header_info["name"] + "';"
		header_id += 1
		print (header_insert)
		#print (header_id)
#
#  Game Data Section
#

	if ('<game name="' in line):
		section = "game"
		game_insert_rows = 'INSERT INTO no-intro_games (system_id, header_id, game_name, category, description) VALUES (' + system_id + ', ' + str(header_id) + ', ' 
		game_insert_values = ''
		
	if (section == "game"):
		tag = '<game name="'
		if (tag in line):
			#print (line[line.index(tag) + len(tag)])
			game_name = line[line.index(tag) + len(tag):line.index('">')]
			game_insert_values = line[line.index(tag) + len(tag):line.index('">')] + '", '
		
		tag = "<category>"
		if (tag in line):
			#category_value = line[line.index(tag) + len(tag):line.index('</')]
			game_insert_values = game_insert_values + '"' + line[line.index(tag) + len(tag):line.index('</')] + '", '
		
		tag = "<description>"
		if (tag in line) and (section == "game"):
			game_insert_values = '"' + game_insert_values + line[line.index(tag) + len(tag):line.index("</")] + '");'
			section = ""

			game_insert = game_insert_rows + game_insert_values
			#game_id = "SELECT id FROM zip_files WHERE name = '" + game_name + "';"
			game_id += 1
			#print (game_insert_rows)
			#print (game_insert_values)
			print (game_insert)
			print (game_id)
#
# ROM Section
#
	tag = '<rom name="'
	if ('<rom name="' in line):
		section = "rom"
		rom_insert = 'INSERT INTO rom_files (system_id, game_id, file_name, size, crc, md5, sha1) VALUES (' + system_id + ', ' + str(game_id) + ', "'

		tag = 'name="'
		tag_end = '" size'
		rom_insert = rom_insert + line[line.index(tag) + len(tag):line.index(tag_end)] + '", "'
		
		tag = 'size="'
		tag_end = '" crc'
		rom_insert = rom_insert + line[line.index(tag) + len(tag):line.index(tag_end)] + '", "'

		tag = 'crc="'
		tag_end = '" md5'
		rom_insert = rom_insert + line[line.index(tag) + len(tag):line.index(tag_end)] + '", "'
		
		tag = 'md5="'
		tag_end = '" sha1'
		rom_insert = rom_insert + line[line.index(tag) + len(tag):line.index(tag_end)] + '", "'

		tag = 'sha1="'
		tag_end = '"/>'
		rom_insert = rom_insert + line[line.index(tag) + len(tag):line.index(tag_end)] + '")'

		print (rom_insert)
		section = ""

dat_file.close()
