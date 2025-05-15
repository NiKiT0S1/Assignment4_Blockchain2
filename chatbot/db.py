from pymongo import MongoClient
from datetime import datetime
import os

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["crypto_ai"]
qa_collection = db["chat_history"]

def save_qa_to_db(question, answer, sources=None):
    """Save question-answer pair to database"""
    qa_collection.insert_one({
        "question": question,
        "answer": answer,
        "sources": sources if sources else [],
        "timestamp": datetime.utcnow()
    })

def get_chat_history(limit=10):
    """Get recent chat history"""
    return list(qa_collection.find().sort("timestamp", -1).limit(limit))

def clear_database():
    """Clear all chat history"""
    qa_collection.delete_many({})