from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from warnings import catch_warnings
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from pydantic.networks import EmailStr

import json
from bson.objectid import ObjectId
from pydantic import BaseModel

import os
from passlib.context import CryptContext
from dotenv import load_dotenv
from config.auth import AuthHandler
load_dotenv()


superAdmin = APIRouter()
auth_handler = AuthHandler()


class logIn(BaseModel):
    password: str


@superAdmin.post("/signin", tags=["admin-auth"])
async def login_account(details: logIn):
    password = details.password
    passwordCheck = auth_handler.verify_password(password)
    if passwordCheck:
        token = auth_handler.encode_token()

        return{"access_token": token, "message": "Welcome, Dr Orji...."}
    else:
        raise HTTPException(
            status_code=400, detail="incorrect password...")
