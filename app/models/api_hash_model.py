import secrets
import string

from app.config import settings
from app.models.bcrypt_model import bcrypt_manager

class APIHashModel:
    """Class to generate"""
    def generate_api_key(self, length: int = settings.api_key_length) -> str:
        """Generate a random API key of a given"""
        alphabet = string.ascii_letters + string.digits
        return "".join(secrets.choice(alphabet) for _ in range(length))

    def hash_api_key(self, api_key: str) -> str:
        """Hash an API key"""
        return bcrypt_manager.hash_password(api_key)
    
    def check_api_hash(self, api_key: str, hashed_key: str) -> bool:
        """Check if an API key matches its hash"""
        return bcrypt_manager.check_password(api_key, hashed_key)

apiHashManager = APIHashModel()

if __name__ == "__main__":
    api_key = apiHashManager.generate_api_key()
    print(f"API Key: {api_key}")
    print(f"Hashed API Key: {apiHashManager.hash_api_key(api_key)}")

