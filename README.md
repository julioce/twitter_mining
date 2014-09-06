Twitter-Mining
==================

A Python Data Mining tool.

Gathers data from Twitter's 100 top celebrities tweets and regular people and saves it to a database

**Steps:**

***run the create_and_insert_users.sql on mysql***


```
$> mysql -u < create_and_insert_users.sql

```

This will create the `twitter_mining` database and the `users` table in MySQL


***Install requirements***

Install de requirements listed in requirements.txt

```
$> pip install -r requirements.txt

```


***run the get_users.py***


```
$> python get_users.py

```

Wait for as long as you want. Every 6 hours the get_users.py will do it's work. You can set the sleep time (horas_sleep) in get_users.py



***check the results on table users and plot k-means***
```
mysql> SELECT * FROM `users`;

$> python k_means.py
```