from config import jwt_secret,jwt_expiry
from dataclasses import dataclass, fields
import datetime
import logging, jwt, re
from flask import request
from functools import wraps

logger = logging.getLogger("cs-proj")
logger.setLevel(logging.DEBUG)


class CustomErrorOne(Exception):
    def __init__(self, e):
        self.e = e


class mainValidation:
    def __init__(self, **kwargs):
        expected_fields = {}
        for i in fields(self):
            expected_fields.update({i.name: i.type})
        for k, v in kwargs.items():
            if not k in expected_fields.keys():
                raise CustomErrorOne(f"Unknown field :{k}")
            if not isinstance(v, expected_fields[k]):
                raise CustomErrorOne(f"Incorrect datatype: {k}")
            setattr(self, k, v)


@dataclass
class User(mainValidation):
    user_name: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__post_init__()

    def __post_init__(self):
        if not ((7 < len(self.user_name) < 11)) or not (self.user_name.isalnum()):
            raise CustomErrorOne(
                "User name must be b/w 8 and 10 and must be alphanumeric"
            )


@dataclass
class Tweet(mainValidation):
    user_id: int
    tweet: str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__post_init__()

    def __post_init__(self):
        if not ((1 < len(self.tweet) < 141)):
            raise CustomErrorOne("Invalid user name")


def validate_keys(data, keys):
    if set(data.keys()) != keys:
        raise (CustomErrorOne("mandatory keys not present"))


def validate_get_tweets(data):
    date = datetime.datetime.strptime(data["date"], "%d-%m-%Y")
    data["date"] = date
    if not isinstance(data["user_name"], str):
        raise CustomErrorOne(f"Incorrect datatype for field: {username}")
    return data


def create_jwt_token(username):
    encoded_jwt = jwt.encode(
        {
            "sub": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=jwt_expiry),
            "iat": datetime.datetime.utcnow(),
        },
        jwt_secret,
        algorithm="HS256",
    )
    return encoded_jwt


def check_header(res=None):
    token = res.headers.get("Authorization")
    if not (token):
        return
    token_match = re.match("^Bearer\s+(.*)", token)
    if not (token_match):
        return
    return token_match.group(1)


def validate_request(fn):
    @wraps(fn)
    def inner(*args, **kwargs):
        token = check_header(res=request)
        if not token:
            raise CustomErrorOne(f"Invalid/No token")
        try:
            payload = jwt.decode(token,jwt_secret,algorithms=["HS256"])
            return fn(*args,**kwargs)
        except jwt.ExpiredSignatureError:
            raise CustomErrorOne('Signature expired.')
        except jwt.InvalidTokenError:
            raise CustomErrorOne('Invalid token')
    return inner
