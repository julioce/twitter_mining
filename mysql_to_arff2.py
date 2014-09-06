import MySQLdb

#mydb = MySQLdb.connect(host="localhost", user="root", passwd="server@bd", db="uso_twitter_mining") 
# Julio
#mydb = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="twitter_mining") 
# Marcus
mydb = MySQLdb.connect(host="127.0.0.1", user="root", passwd="server@bd", db="twitter_mining") 
cursor = mydb.cursor()

def user_by_tweets():

	
	statement = """SELECT 	users.id, users.user_id, users.screen_name, ((max_user_data.followers_count / min_user_data.followers_count)- 1)*100 AS percentagem,
	(max_user_data.followers_count - min_user_data.followers_count) AS num_followers
	
	FROM users 	
		JOIN ( SELECT MAX(date_time) AS max_date_time, MIN(date_time) AS min_date_time, user_id FROM users GROUP BY user_id)
			AS date_user ON date_user.user_id = users.user_id
		JOIN ( SELECT friends_count, followers_count, statuses_count, date_time, user_id FROM users ) 
			AS max_user_data ON max_user_data.date_time = date_user.max_date_time AND max_user_data.user_id = date_user.user_id
		JOIN ( SELECT friends_count, followers_count, statuses_count, date_time, user_id FROM users ) 
			AS min_user_data ON min_user_data.date_time = date_user.min_date_time AND min_user_data.user_id = date_user.user_id
	WHERE  (max_user_data.followers_count - min_user_data.followers_count) > 0	 AND users.screen_name != 'charliesheen' 	

	GROUP BY users.user_id

	ORDER BY percentagem DESC;"""

	cursor.execute(statement)
	rows = cursor.fetchall()
	arff_string_file = """@relation tweet
@attribute 'id' real
@attribute 'twitter_id' real
@attribute 'username' string
@attribute 'percentagem' real
@attribute 'num_followers' real
@data
"""

	myFile = open('input_file.arff', 'w')

	for row in rows:
		arff_string_file += """%s,%s,'%s',%s,%s\n""" % (row[0],row[1],row[2],row[3],row[4])

	myFile.write(arff_string_file)
	myFile.close()
