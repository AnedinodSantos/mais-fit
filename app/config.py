import os

DB = "mysql"# os.environ.get("DB")
USER = "root" # os.environ.get("USER")
PASS = "dinossauro12"# os.environ.get("PASS")
DB_URL = "localhost/mais_fit"# os.environ.get("DB_URL")

connect_string = f'{DB}://{USER}:{PASS}@{DB_URL}'
config = {
    'db.url': connect_string,
    'db.echo':'True'
}