from fastapi import APIRouter, HTTPException, Response, status, Depends

from .documents import User
from .models import SignupModel
from .services.auth_helpers import get_current_user, hash_password, create_jwt_token, authenticate_user

router = APIRouter(prefix="/auth/api/users")


@router.get("/current/user")
async def current_user(user: User = Depends(get_current_user)):
    return {"id": str(user.id), "email": user.email}


@router.post("/signup", status_code=201)
async def signup(request_data: SignupModel, response: Response):
    if await User.find_one({"email": request_data.email}):
        raise HTTPException(detail="Email is already taken", status_code=400)
    hashed_password = hash_password(request_data.password)
    user = User(email=request_data.email, password=hashed_password)
    saved_user = await user.save()
    jwt_token = create_jwt_token({"id": str(saved_user.id), "email": saved_user.email})
    response.set_cookie(key="token", value=jwt_token)
    return {"id": str(saved_user.id), "email": saved_user.email}


@router.post("/login")
async def login(sign_in_data: User, response: Response):
    user = await authenticate_user(sign_in_data.email, sign_in_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    jwt_token = create_jwt_token({"id": str(user.id), "email": user.email})
    response.set_cookie(key="token", value=jwt_token)
    return {"id": str(user.id), "email": user.email}


@router.post("/sign/out")
async def sing_out(response: Response):
    response.delete_cookie(key="token")
    return {}

