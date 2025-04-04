import os

# Stores all configuration values
SECRET_KEY = os.urandom(16)
MONGODB_HOST = os.environ.get('MONGODB_HOST')

'mongodb+srv://aramzap:showpony@cluster0.agpqikk.mongodb.net/cmsc388j?retryWrites=true&w=majority&appName=Cluster0'