from uuid import uuid4
from hashlib import blake2b, sha512
from django.utils.timezone import datetime, timedelta, now
from django.conf import settings
import os
import jwt


def hash_key(key):
    return sha512(key.encode()).hexdigest()


def check_key(key, hashed):
    return hash_key(key) == hashed


def generate_uid():
    return uuid4()


def generate_token(key, refresh, token_id, public_id, token_type=None, lifetime=None):
    if token_type == "superuser":
        lifetime = 5
    elif lifetime is None:
        lifetime = settings.JWT_TOKEN_VALIDITY_TIME

    token_auth = _generate_token_jwt(
        key, 
        public_id, 
        token_type, 
        token_id, 
        lifetime)

    token_refresh = _generate_token_jwt(
        refresh,
        public_id, 
        token_type, 
        token_id, 
        settings.JWT_REFRESH_TOKEN_VALIDITY_TIME
        )
    return token_auth, token_refresh



def _generate_token_jwt(key, id_, role, token_id, lifetime):
    payload = {
        "key": hash_key(key),
        "exp": datetime.utcnow() + timedelta(minutes=lifetime),
        "id": id_,
        "token": token_id,
        "role": role,
        "iat": datetime.utcnow(),
        "iss": os.getenv("APP_URL", "localhost")
    }
    return jwt.encode(payload, hash_key(settings.JWT_SECRET), algorithm="HS256")


def validate_jwt(token_jwt):
    try:
        payload = jwt.decode(
            token_jwt, hash_key(settings.JWT_SECRET),
            issuer=os.getenv("APP_URL", "localhost"),
            options={"required": ["exp", "iat", "iss"]},
            algorithms=["HS256"],
        )
    except (
        jwt.ExpiredSignatureError,
        jwt.DecodeError,
        jwt.InvalidIssuerError,
        jwt.MissingRequiredClaimError,
        jwt.InvalidIssuedAtError
    ):
        return {}
    else:
        return payload
