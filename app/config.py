import os

from dotenv import load_dotenv

# Sets the base directory path
basedir = os.path.abspath(os.path.dirname(__file__))

# loads the environment variable file
load_dotenv()


# Function to get the environmental variables
def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected env variable '{}' not set.".format(name)
        raise Exception(message)


# Set the variables
POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")
SECRET_KEY_ENV = get_env_variable("SECRET_KEY")

DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER, pw=POSTGRES_PW, url=POSTGRES_URL,
                                                      db=POSTGRES_DB)


# db_string = "postgresql://postgres:postgres@localhost/metrologie"

# Sets the database
class Config(object):
    SECRET_KEY = SECRET_KEY_ENV or 'secret key'
    SQLALCHEMY_DATABASE_URI = DB_URL or \
                              'psql:///' + os.path.join(basedir)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
