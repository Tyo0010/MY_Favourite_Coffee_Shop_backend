import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This load_dotenv call is mainly for local development.
# In Lambda, Zappa will set environment variables directly.
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    # Default SQLALCHEMY_DB_ECHO to False in production, allow override via env var
    SQLALCHEMY_DB_ECHO = os.environ.get('SQLALCHEMY_DB_ECHO', 'False').lower() in ('true', '1', 't')
    SQLALCHEMY_TRACK_MODIFICATIONS = False