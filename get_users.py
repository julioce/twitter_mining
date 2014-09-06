# -*- coding: utf-8 -*-
from exceptions import Exception
from datetime import datetime
from time import time, sleep
import MySQLdb
import tweepy

mydb = MySQLdb.connect(host="localhost", user="root", passwd="server@bd", db="uso_twitter_mining") 
# julio
# mydb = MySQLdb.connect(host="localhost", user="root", passwd="", db="twitter_mining") 
cursor = mydb.cursor()

consumer_key="eSWSQWbtOxtj5DJYz9I7dQ"
consumer_secret="B3SPTXqFrgW4c4SsqrQlyyXuvQWTzdxyD6S8nI"
access_token="21413905-w8BSeCPoLgxvCFFPJuT3j068dL7UeMVNCAuvMKpQ"
access_token_secret="PDeZeCxVbTmMjC5rO9wT6iP2eRiJr2PrmstlnZOo"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

usuarios = [ 'marcuscouto', 'bueno_julio','justinbieber', 'ladygaga', 'katyperry', 'BarackObama', 'rihanna', 'YouTube', 'taylorswift13', 'britneyspears', 'shakira', 'jtimberlake', 'instagram', 'TheEllenShow', 'twitter', 'Oprah', 'Cristiano', 'JLo', 'KimKardashian', 'NICKIMINAJ', 'BrunoMars', 'Pink', 'KAKA', 'selenagomez', 'Eminem', 'aplusk', 'OfficialAdele', 'ddlovato', 'aliciakeys', 'Harry_Styles', 'chrisbrown', 'onedirection', 'twitter_es', 'MileyCyrus', 'cnnbrk', 'LilTunechi', 'NiallOfficial', 'BillGates', 'Drake', 'Pitbull', 'ParisHilton', 'MariahCarey', 'SnoopDogg', 'Louis_Tomlinson', 'JimCarrey', 'Real_Liam_Payne', 'AvrilLavigne', 'UberSoc', 'coldplay',  'RyanSeacrest', 'wizkhalifa', 'ashleytisdale', 'kanyewest', 'charliesheen', 'tyrabanks', 'AlejandroSanz', 'zaynmalik', 'iamdiddy', 'TwitPic', 'FCBarcelona', 'davidguetta', 'KourtneyKardash', 'jimmyfallon', 'ricky_martin', 'CNN', 'nytimes', 'ConanOBrien', 'KingJames', 'facebook', 'danieltosh', 'KhloeKardashian', 'MTV', 'ivetesangalo', 'Beyonce', 'paulocoelho', '50cent',  'juanes', 'realmadrid', 'agnezmo', 'Usher', 'Ludacris', 'KevinHart4real', 'programapanico', 'EmWatson', 'NBA', 'SHAQ', 'DalaiLama', 'iamwill', 'ClaudiaLeitte', 'SimonCowell', 'carlyraejepsen', 'LucianoHuck', 'Njr92', 'paurubio', 'Anahi', 'tomhanks', 'JessicaSimpson', 'rustyrockets', 'espn', 'edsheeran', 'JessieJ', 'WayneRooney' ]

# Formata da data enviada pelo Twitter para MySQL
def twitter_date_to_mysql(twitter_date):
	return datetime.strptime(twitter_date.strip('"'), "%a %b %d %H:%M:%S +0000 %Y")

# Procura os status do username e retorna um array com as informações 
def user_detail(user):
	
	try:
		dados = api.get_user(user)
		user_id = dados.id
		created_at =  dados.created_at
		screen_name = dados.screen_name
		friends_count = dados.friends_count
		followers_count = dados.followers_count
		statuses_count = dados.statuses_count

		return [ str(user_id), str(created_at), str(screen_name), str(friends_count), str(followers_count), str(statuses_count) ]
				
	except:
		print """Erro ao acessar dados do usuario %s""" % user
		# Nova tentativa em 10 minutos 
		nova_tentativa = 10
		print """Nova tentativa em %s minutos""" % nova_tentativa
		sleep(nova_tentativa*60)
		return user_detail(user)

def  load_users():

	for user in usuarios:
		print "'", user, "' inserido às ", datetime.now()
		lista_atributos = user_detail(user)
		#print lista_atributos

		statement = """INSERT INTO users(id, user_id, created_at, screen_name, friends_count, followers_count, statuses_count, date_time) VALUES(DEFAULT, '%s', '%s', '%s', '%s', '%s', '%s', NOW());"""%( lista_atributos[0], lista_atributos[1], lista_atributos[2], lista_atributos[3], lista_atributos[4], lista_atributos[5])
		cursor.execute(statement)
		mydb.commit()

#Dorme por 6horas = 60sec*60min*1
horas_sleep = 6
tempo_sleep = 60*60*horas_sleep

# Iterador de hora em hora
while True:
	print "Nova iteração iniciando em", datetime.now()
	load_users()
	
	print "\nDormindo por", horas_sleep, "hora(s)...."
	sleep(tempo_sleep)