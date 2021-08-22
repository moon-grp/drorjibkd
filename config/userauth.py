
import os
from fastapi import security
import jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()




token_secret = os.getenv("JWT_aff_KEY")
o_pass = os.getenv("PASSCODE")


class AuthHandler():
    security = HTTPBearer()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret = token_secret

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hash_password):
        return self.pwd_context.verify(plain_password, hash_password)

    def encode_token(self, phonenum):
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, minutes=30),
            "iat": datetime.utcnow(),
            "sub": phonenum
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret, algorithms=["HS256"])
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=401, detail="token has expired")
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail="invalid token")

    def auth_wrapper(self, auth: HTTPAuthorizationCredentials = Security(security)):
        return self.decode_token(auth.credentials)

