from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    
    user_id = db.Column(db.Integer, nullable=False)
    plan_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default="pending")
    paypal_subscription_id = db.Column(db.String(100), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
