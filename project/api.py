from flask import Flask, request, jsonify
from utils import (
    User,
    Tweet,
    CustomErrorOne,
    validate_keys,
    validate_get_tweets,
    create_jwt_token,
    validate_request
)
from werkzeug.exceptions import MethodNotAllowed, BadRequest
from sqlalchemy.exc import IntegrityError

from db import (
    create_user_in_db,
    create_tweet_in_db,
    get_tweets_from_db,
    delete_tweets_from_db,
)

app = Flask(__name__)

@app.post("/user")
def create_user():
    if not request.json:
        raise CustomErrorOne("Required Data not present")
    user = User(**request.json)
    result = create_user_in_db(user)
    result['token'] = create_jwt_token(user.user_name)
    return result, 200


@app.post("/tweet")
@validate_request
def create_tweet():
    if not request.json:
        raise CustomErrorOne("Required Data not present")
    tweet = Tweet(**request.json)
    result = create_tweet_in_db(tweet)
    return result, 200


@app.get("/tweets")
@validate_request
def get_tweets():
    data = dict(request.args)
    validate_keys(data, {"user_name", "date"})
    data = validate_get_tweets(data)
    result = get_tweets_from_db(data)
    return jsonify({"tweets": result, "count": len(result)}), 200


@app.delete("/tweets/<username>")
@validate_request
def delete_tweets(username):
    result = delete_tweets_from_db(username)
    return jsonify({"tweets": result, "count": len(result)}), 200

@app.errorhandler(CustomErrorOne)
def send_client_error(e):
    return jsonify({"error": e.args[0]}), 400


@app.errorhandler(ValueError)
def send_client_error(e):
    return jsonify({"error": e.args[0]}), 400


@app.errorhandler(IntegrityError)
def send_db_error(e):
    val = e.params.get("user_id") or e.params.get("user_name")
    return (
        jsonify({"error": f"key {val} already/doesnot exists in database"}),
        500,
    )

@app.errorhandler(BadRequest)
def send_bad_request(e):
    return jsonify({"error": e.description}), e.code


@app.errorhandler(MethodNotAllowed)
def send_method_not_allowed(e):
    return jsonify({"error": e.description}), e.code


@app.errorhandler(Exception)
def handle_every_error(e):
    if hasattr(e, "description") and hasattr(e, "code"):
        return jsonify({"error": e.description}), e.code
    return jsonify({"error": "Unhandled error"}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)
