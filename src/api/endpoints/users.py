from fastapi import APIRouter, Depends, Response
from fastapi.responses import RedirectResponse
from typing import List
from pymongo.mongo_client import MongoClient
import db
from models.user import UserOut, CreateUserIn, UserInDB, UpdateUserIn
from core.security import (
    get_password_hash,
    get_current_active_user,
    get_current_active_superuser,
)
from endpoints.helpers_tools.common_dependencies import QuerySearchPageParams
from endpoints.helpers_tools.user_dependencies import (
    validate_accept_terms_of_service,
    validate_username_and_email_not_in_db,
    validate_current_user_edit_itself,
    validate_match_password,
)

router = APIRouter()


@router.get(
    "/",
    response_model=List[UserInDB],
    dependencies=[Depends(get_current_active_superuser)],
    summary="Get all users",
    description="Get all users. Only superusers can do this.",
)
async def read_users(
    db: MongoClient = Depends(db.get_db),
    search_params: QuerySearchPageParams = Depends(QuerySearchPageParams),
):
    return list(db.users.find({}).skip(search_params.skip).limit(search_params.limit))


@router.get(
    "/me",
    response_class=RedirectResponse,
    summary="Get current user",
    description="Redirect to user profile",
)
async def read_current_user(
    current_user: UserOut = Depends(get_current_active_user),
):
    return current_user.username


@router.get(
    "/{username}",
    response_model=UserOut,
    summary="User page",
    description="Get user basic data",
)
async def read_user(
    username: str,
    db: MongoClient = Depends(db.get_db),
):
    # TODO: return 404 if user not found
    user = db.users.find_one({"username": username})
    return user


@router.put(
    "/{username}",
    status_code=204,
    summary="Update current user",
    description="Update current user with shown fields",
    dependencies=[Depends(validate_current_user_edit_itself)],
)
async def update_user(
    username: str,
    user_in: UpdateUserIn,
    db: MongoClient = Depends(db.get_db),
):
    # TODO: return 404 if user not found
    db.users.update_one(
        {"username": username},
        {"$set": user_in.dict(exclude_none=True, exclude_unset=True)},
    )
    return Response(status_code=204)


@router.post(
    "/",
    status_code=201,
    dependencies=[
        Depends(validate_accept_terms_of_service),
        Depends(validate_username_and_email_not_in_db),
        Depends(validate_match_password),
    ],
)
async def create_user(
    user_in: CreateUserIn,
    db: MongoClient = Depends(db.get_db),
):
    # TODO: add additional responses
    # TODO: add email verification

    # * hash the password
    hash_password = get_password_hash(user_in.password.get_secret_value())

    # * setup userInDB with hash password
    userInDB = UserInDB(**user_in.dict(exclude={"password"}), password=hash_password)

    # * insert user
    db.users.insert_one(userInDB.dict())

    return Response(status_code=201)
