import MySQLdb

#mydb = MySQLdb.connect(host="localhost", user="root", passwd="server@bd", db="uso_twitter_mining") 
# Julio
mydb = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="twitter_mining") 
# Marcus
# mydb = MySQLdb.connect(host="127.0.0.1", user="root", passwd="server@bd", db="twitter_mining") 
cursor = mydb.cursor()

def user_by_tweets():

	statement = """SELECT 	users.id, users.user_id, users.screen_name, 
	min_date_time AS start_time, max_date_time AS end_time, 
	max_user_data.friends_count AS friends_count_end, min_user_data.friends_count AS friends_count_start, 
	max_user_data.followers_count AS followers_count_end, min_user_data.followers_count AS followers_count_start, 
	max_user_data.statuses_count AS statuses_count_end, min_user_data.statuses_count AS statuses_count_start
	
	FROM users 	
		JOIN ( SELECT MAX(date_time) AS max_date_time, MIN(date_time) AS min_date_time, user_id FROM users GROUP BY user_id)
			AS date_user ON date_user.user_id = users.user_id
		JOIN ( SELECT friends_count, followers_count, statuses_count, date_time, user_id FROM users ) 
			AS max_user_data ON max_user_data.date_time = date_user.max_date_time AND max_user_data.user_id = date_user.user_id
		JOIN ( SELECT friends_count, followers_count, statuses_count, date_time, user_id FROM users ) 
			AS min_user_data ON min_user_data.date_time = date_user.min_date_time AND min_user_data.user_id = date_user.user_id
				
	GROUP BY users.user_id;"""


	cursor.execute(statement)
	rows = cursor.fetchall()
	arff_string_file = """@relation tweet
@attribute 'id' real
@attribute 'twitter_id' real
@attribute 'username' string
@attribute 'data_end' string
@attribute 'data_start' string
@attribute 'friend_count_end' real
@attribute 'friend_count_start' real
@attribute 'folowers_end' real
@attribute 'folowers_start' real
@attribute 'statuses_end' real
@attribute 'statuses_start' real
@data
"""

	myFile = open('input_file.arff', 'w')

	for row in rows:
		arff_string_file += """%s,%s,'%s','%s','%s',%s,%s,%s,%s,%s,%s\n""" % (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10])

	myFile.write(arff_string_file)
	myFile.close()
