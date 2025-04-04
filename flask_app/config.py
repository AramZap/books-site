import os

# Stores all configuration values
SECRET_KEY = os.urandom(16)
MONGODB_HOST = os.environ.get('MONGODB_HOST')