from beanie import Document
from pydantic import EmailStr, validator


class User(Document):
    email: EmailStr
    password: str
