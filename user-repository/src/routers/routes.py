import logging
from fastapi import APIRouter, Depends
from src.models.user import User
from src.mongodb_client import get_user_service
from src.service.user_services import UserService


router = APIRouter(
    prefix="/api/v1/users"
)

@router.get("/{email}", status_code=200)
async def find_user(email: str, user_service: UserService = Depends(get_user_service)):
    ''' Get user '''
    return await user_service.get_user(email=email)


@router.post("/", status_code=201)
async def add_user(user: User, user_service: UserService = Depends(get_user_service)):
    ''' Get user '''
    logging.info("====> add user, %s", user )
    return await user_service.add_user(user)

@router.put("/{email}", status_code=201)
async def update_user(user: User, user_service: UserService = Depends(get_user_service)):
    ''' Get user '''
    return await user_service.update_user(user)


@router.delete("/{email}", status_code=201)
async def delete_user(email: str, user_service: UserService = Depends(get_user_service)):
    ''' Get user '''
    return await user_service.delete_user(email=email)
