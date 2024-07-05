"""This module contains the authentication model for the web application that communicates with the frontend"""
from datetime import datetime, timedelta, timezone

from pydantic import BaseModel
from jose import jwt, JWTError

from app.config import settings
from app.views.users_schema import UserSchema

class TokenData(BaseModel):
    username: str | None = None

class AuthModel:
    def __init__(self):
        self.secret_key = settings.jwt_secret
        self.algorithm = settings.jwt_algorithm
        self.access_token_expire_minutes = settings.jwt_expiration

    def create_access_token(self, data: dict):
        """Create an access token with the given data"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    def create_access_token_from_user(self, user: UserSchema):
        """
        Create an access token from a user instance.
        The token will contain in the payload:
            - sub: the user_id in the database
            - exp: the expiration time of the token
        """

        if not isinstance(user, UserSchema):
            raise TypeError("User must be an instance of UserSchema")

        data = {
            "sub": user.id,
            }
        return self.create_access_token(data)

    def decode_token(self, token: str):
        """Decode a token and return its payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            return None

    def verify_token(self, token: str) -> bool:
        """Verify if a token is valid"""
        payload = self.decode_token(token)
        if payload:
            username: str = payload.get("sub")
            if username is None:
                return False
            return True
        return False


authHandler = AuthModel()

if __name__ == "__main__":
    token = authHandler.create_access_token(data={"sub": "username"})
    print(token)
    print(authHandler.decode_token(token))
    print(authHandler.verify_token(token))
    print(authHandler.verify_token("invalid_token"))
    print(authHandler.decode_token("invalid_token"))