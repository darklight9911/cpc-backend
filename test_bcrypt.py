from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    hash = pwd_context.hash("secret")
    print(f"Hash created successfully: {hash}")
    verify = pwd_context.verify("secret", hash)
    print(f"Verification result: {verify}")
except Exception as e:
    print(f"Error: {e}")
