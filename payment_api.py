from flask import Flask, request, jsonify
from paypalrestsdk import BillingAgreement
import paypalrestsdk
from models import db, Subscription
from config import Config
from utils import verify_token
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

paypalrestsdk.configure({
    "mode": os.getenv("PAYPAL_MODE", "sandbox"),
    "client_id": os.getenv("PAYPAL_CLIENT_ID"),
    "client_secret": os.getenv("PAYPAL_CLIENT_SECRET")
})

with app.app_context():
    db.create_all()

@app.route('/api/subscribe', methods=['POST'])
def create_subscription():
    token = request.headers.get("Authorization")
    user_id = verify_token(token)
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    plan_type = data.get("plan_type")
    if plan_type not in ["premium", "basic"]:
        return jsonify({"error": "Invalid plan type"}), 400

    plan_id = os.getenv("PAYPAL_PLAN_ID")

    agreement = BillingAgreement({
        "name": "Subscription Plan",
        "description": f"{plan_type.capitalize()} Subscription Plan",
        "start_date": "2025-03-01T00:00:00Z",
        "plan": {
            "id": plan_id
        },
        "payer": {
            "payment_method": "paypal"
        }
    })

    if agreement.create():
        approval_url = next(link.href for link in agreement.links if link.rel == "approval_url")
        subscription = Subscription(user_id=user_id, plan_type=plan_type, status="pending", paypal_subscription_id=agreement.id)
        db.session.add(subscription)
        db.session.commit()
        return jsonify({"approval_url": approval_url})
    else:
        return jsonify({"error": agreement.error}), 400

@app.route('/api/webhook', methods=['POST'])
def paypal_webhook():
    data = request.json
    event_type = data.get("event_type")
    
    if event_type == "BILLING.SUBSCRIPTION.ACTIVATED":
        subscription_id = data["resource"]["id"]
        subscription = Subscription.query.filter_by(paypal_subscription_id=subscription_id).first()
        if subscription:
            subscription.status = "active"
            db.session.commit()
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.getenv("PORT", 5000)))
