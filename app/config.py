import os


DB = os.environ.get("DB")
USER = os.environ.get("USER")
PASS = os.environ.get("PASS")
DB_URL = os.environ.get("DB_URL")

connect_string = f'{DB}://{USER}:{PASS}@{DB_URL}'
config = {
    'db.url': connect_string,
    'db.echo':'True'
}