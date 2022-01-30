from sqlalchemy import create_engine, MetaData, Table, select, and_
import sys
from config import connectionstring,debug
from utils import logger

try:
    engine = create_engine(
        connectionstring,
        echo=debug,
        future=True,
    )
    metadata = MetaData()
    with engine.connect() as conn:
        user_table = Table("cs_user", metadata, autoload_with=conn)
        tweet_table = Table("cs_tweet", metadata, autoload_with=conn)
except Exception as e:
    logger.error(e)
    sys.exit()

def create_user_in_db(user):

    data = {"user_name": user.user_name}
    statement = user_table.insert().values(data).return_defaults()
    with engine.begin() as conn:
        result = conn.execute(statement)
    return {
        "user_id": result.returned_defaults[0],
        "created_timestamp": result.returned_defaults[1],
    }

def create_tweet_in_db(tweet):
    data = {"user_id": tweet.user_id, "tweet": tweet.tweet}
    statement = tweet_table.insert().values(data).return_defaults()
    with engine.begin() as conn:
        result = conn.execute(statement)
    return {
        "tweet_id": result.returned_defaults[0],
        "created_timestamp": result.returned_defaults[1],
    }


def get_tweets_from_db(data):
    join_table = tweet_table.join(user_table)
    statement = (
        select(tweet_table.c.tweet)
        .select_from(join_table)
        .where(
            and_(
                user_table.c.user_name == data["user_name"],
                tweet_table.c.created_timestamp > data["date"],
            )
        )
    )
    with engine.connect() as conn:
        result = [i.tweet for i in conn.execute(statement).fetchall()]
    return result


def delete_tweets_from_db(user_name):
    select_statement = select(user_table.c.user_id).where(
        user_table.c.user_name == user_name
    )
    response = []
    with engine.begin() as conn:
        user = conn.execute(select_statement).fetchone()
        result = []
        if user:
            delete_statement = (
                    tweet_table.delete()
                    .where(tweet_table.c.user_id == user.user_id)
                    .returning(tweet_table.c.tweet_id, tweet_table.c.tweet)
                )
            result = conn.execute(delete_statement)         
    for tweet_id, tweet in result:
        response.append({tweet_id: tweet})
    return response
