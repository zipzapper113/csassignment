import os

connectionstring = os.getenv(
    "connection_string", "postgresql+psycopg2://testuser:admin@172.18.0.1:54320/postgres"
)
debug = False

jwt_secret = os.getenv("secret_key","secret")
jwt_expiry = 60 #(minutes)