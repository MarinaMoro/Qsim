from pymongo import MongoClient

# Подключение к MongoDB
client = MongoClient('localhost', 27017)

db = client['qtlab_projects']

projects_collection = db["projects"]