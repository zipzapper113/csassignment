1)Setting up the database

I have used  postgresql as db, tables can be created via running db_script.py or by below SQL Queries
Note: i) uuid extension must be enabled for creating cs_tweet table, can install via command: CREATE EXTENSION "uuid-ossp";
      ii)to create via python script, asyncio supported python version has to be present as we have used asyncpg driver and for actual
          project used sync driver psycopg2.

CREATE TABLE cs_user (
	user_id SERIAL NOT NULL, 
	user_name VARCHAR(10) NOT NULL, 
	created_timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
	PRIMARY KEY (user_id), 
	UNIQUE (user_name)
)

CREATE TABLE cs_tweet (
	tweet_id UUID DEFAULT uuid_generate_v4() NOT NULL, 
	tweet VARCHAR(140) NOT NULL, 
	created_timestamp TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (tweet_id), 
	FOREIGN KEY(user_id) REFERENCES cs_user (user_id)
)

2)Hosted the backend & db on below host

Url: https://madhavcs.centralus.cloudapp.azure.com

Routes: 
i)Create user
curl -XPOST -H "Content-type: application/json" -d '{"user_name" : "madhav1234"}' 'https://madhavcs.centralus.cloudapp.azure.com/user'

ii)Create tweet
curl -XPOST -H 'Authorization:Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtYWRoYTEyMzQiLCJleHAiOjE2NDM1NTE0NjIsImlhdCI6MTY0MzU0Nzg2Mn0.-6eLK72tqyEbuC29UNkd0sEe9aNvzNi6rnDoQme3las' -H "Content-type: application/json" -d '{"user_id" : 4, "tweet" : "hello" }' 'https://madhavcs.centralus.cloudapp.azure.com/tweet'

iii)list tweets from particular date
curl -XGET -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtYWRoYTEyMzQiLCJleHAiOjE2NDM1NTE0NjIsImlhdCI6MTY0MzU0Nzg2Mn0.-6eLK72tqyEbuC29UNkd0sEe9aNvzNi6rnDoQme3las' -H "Content-type: application/json" 'https://madhavcs.centralus.cloudapp.azure.com/tweets?date=01-01-2022&user_name=madhav1234'

iv)Delete tweets for a user
curl -XDELETE -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtYWRoYTEyMzQiLCJleHAiOjE2NDM1NTE0NjIsImlhdCI6MTY0MzU0Nzg2Mn0.-6eLK72tqyEbuC29UNkd0sEe9aNvzNi6rnDoQme3las' -H "Content-type: application/json" 'https://madhavcs.centralus.cloudapp.azure.com/tweets/madhav1234'

