from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    name: constr(min_length=1, max_length=100)
    uni_id: constr(pattern=r"^[0-9-]+$", max_length=100)
    email: EmailStr
    password: constr(min_length=6)

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    name: str
    uni_id: str
    email: EmailStr

    class Config:
        from_attributes = True

class OTPVerify(BaseModel):
    email: EmailStr
    otp: str
    registration_data: UserCreate

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
