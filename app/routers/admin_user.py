from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated, List
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from ..database import get_db
from ..authentication import users_oauth
from ..models.users_model import User
from ..schemas import users_schema




router = APIRouter(
    prefix="/admin",
    tags=["Admin_Dashbord"]
)


@router.get("/users", response_model=List[users_schema.UserAdminListItem])
def get_all_users(
    admin: Annotated[User, Depends(users_oauth.get_current_admin_user)],
    db: Annotated[Session, Depends(get_db)]
):
    users = db.query(User).all()
    return users