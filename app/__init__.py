from flask import Flask
from pymongo import MongoClient
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.mongo_client = MongoClient(app.config['MONGO_URI'])
    app.mongo_db = app.mongo_client.get_default_database()
    
    # Test connection
    try:
        app.mongo_db.command('ping')
        print(" MongoDB connected...")
        
        # CREATE INDEXES HERE (right after connection verification)
        app.mongo_db.events.create_index([('timestamp', -1)])  # For sorting by timestamp
        app.mongo_db.events.create_index([('action', 1)])      # For filtering by action type
        print(" MongoDB indexes created")
        
    except Exception as e:
        print(f" MongoDB connection Failed... {e}")
        raise

    from app.routes import bp
    app.register_blueprint(bp)
    
    return app