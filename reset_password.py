import asyncio
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.core.security import get_password_hash

async def reset_password(email, new_password):
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalars().first()
        
        if user:
            print(f"User found: {user.name} ({user.email})")
            hashed_pw = get_password_hash(new_password)
            user.password_hash = hashed_pw
            db.add(user)
            await db.commit()
            print(f"Password reset successfully to: {new_password}")
        else:
            print("User not found!")

if __name__ == "__main__":
    target_email = "iman241-15-540@diu.edu.bd"
    temp_password = "123456"
    asyncio.run(reset_password(target_email, temp_password))
