from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.session import get_db, get_redis
from app.models.user import User
from app.schemas.user import UserCreate, OTPVerify
from app.core.config import settings
import httpx
import random
import uuid

router = APIRouter()

@router.post("/register", status_code=status.HTTP_200_OK)
async def register(
    user_in: UserCreate, 
    db: AsyncSession = Depends(get_db),
    redis = Depends(get_redis)
):
    # 1. Check if user already exists
    result = await db.execute(select(User).where((User.email == user_in.email) | (User.uni_id == user_in.uni_id)))
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this Email or University ID already exists",
        )
    
    # 2. Email Validation (@diu.edu.bd) - handled by Schema but double checking logic if needed
    if not user_in.email.endswith("@diu.edu.bd"):
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email must be a DIU student email (@diu.edu.bd)",
        )

    # 3. Generate OTP
    otp_code = str(random.randint(100000, 999999))
    
    # 4. Store in Redis (TTL 5 mins = 300s)
    await redis.setex(f"otp:{user_in.email}", 300, otp_code)
    
    # 5. Send to Discord
    async with httpx.AsyncClient() as client:
        message = {
             "content": f"🔐 **New OTP Request**\n**User:** {user_in.name} ({user_in.uni_id})\n**Email:** {user_in.email}\n**OTP:** `{otp_code}` 🚀"
        }
        await client.post(settings.DISCORD_WEBHOOK_URL, json=message)
        
    return {"message": "OTP sent successfully. Please check your Discord/Email."}

@router.post("/verify", status_code=status.HTTP_201_CREATED)
async def verify_otp(
    otp_in: OTPVerify,
    db: AsyncSession = Depends(get_db),
    redis = Depends(get_redis)
):
    # 1. Retrieve OTP from Redis
    stored_otp = await redis.get(f"otp:{otp_in.email}")
    
    if not stored_otp or stored_otp != otp_in.otp:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP",
        )
        
    # 2. Create User
    new_user = User(
        name=otp_in.registration_data.name,
        uni_id=otp_in.registration_data.uni_id,
        email=otp_in.registration_data.email,
        password_hash=otp_in.registration_data.password # In production, hash this!
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # 3. Clean up OTP
    await redis.delete(f"otp:{otp_in.email}")
    
    return {"message": "Registration successful!", "user_id": str(new_user.id)}
