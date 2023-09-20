from pydantic import BaseModel, EmailStr, validator


class SignupModel(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def password_validator(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be between 8 and 20 characters")
        return v


class SignInModel(BaseModel):
    email: EmailStr
    password: str

    @validator("password")
    def password_validator(cls, v):
        if len(v) == 0:
            raise ValueError("You must supply a password")
