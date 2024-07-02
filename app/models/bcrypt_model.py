import os
import bcrypt

from app.config import settings

class Bcrypt:
    def __init__(self):
        self.rounds = 12

    def generate_salt(self):
        return bcrypt.gensalt(rounds=self.rounds)

    def hash_password(self, password: str) -> str:
        salt = self.generate_salt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    def check_password(self, password: str, hashed: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
bcrypt_manager = Bcrypt()

if __name__ == "__main__":

    # Criar hash de uma senha
    password = "minha_senha_segura"
    hashed_password = bcrypt_manager.hash_password(password)
    print(f"Senha hasheada: {hashed_password}")
    
    # Verificar uma senha
    is_correct = bcrypt_manager.check_password(password, hashed_password)
    print(f"A senha está correta? {is_correct}")
    
    # Atualizar o número de rounds
    bcrypt_manager.update_rounds(14)
    print(f"Número de rounds atualizado para: {bcrypt_manager.rounds}")