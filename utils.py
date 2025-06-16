import jwt
from datetime import datetime, timedelta
from config import Config

def verify_token(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except:
        return None
