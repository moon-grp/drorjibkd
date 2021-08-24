
from datetime import datetime, timedelta
from model.superadmin import Signupauth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from warnings import catch_warnings
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from pydantic.networks import EmailStr

import json
from bson.objectid import ObjectId
from pydantic import BaseModel
from model.users.createacc import Account
from model.superadmin import Signupauth
import os
from passlib.context import CryptContext
from dotenv import load_dotenv
import validators
from config.userauth import AuthHandler
load_dotenv()


aff = APIRouter()
auth_handler = AuthHandler()


class Newaccount(BaseModel):
    username: str
    email: str
    password: str


class logIn(BaseModel):
    phn: str
    password: str


class signup(BaseModel):
    #phn: str
    password: str
    passcode: str


@aff.post("/signin", tags=["users"])
async def login_account(details: logIn):
    phonum = details.phn
    password = details.password
    if len(details.phn) > 11 or len(details.phn) < 11:
        raise HTTPException(
            status_code=400, detail="phone number longer or shorter than 11..")
    else:
        try:
            checkE = json.loads(Account.objects.get(
                phonenumber=phonum).to_json())
            passwordCheck = auth_handler.verify_password(
                password, checkE["password"])
            if passwordCheck:
                token = auth_handler.encode_token(phonum)

                return{"access_token": token, "token_type": "bearer"}
            else:
                raise HTTPException(
                    status_code=400, detail="invalid password")

        except Account.DoesNotExist:
            raise HTTPException(
                status_code=400, detail="Account does not exist")


@aff.post("/signup", tags=["users"])
async def create_account(details: signup):
    #phnum = details.phn
    try:
        checkPasscode = json.loads(Signupauth.objects.get(
            authcode=details.passcode).to_json())
        getauthdetails = Signupauth.objects.get(
            authcode=details.passcode)
        getphone = getauthdetails.phonenumber

        try:
            checkE = json.loads(Account.objects.get(
                phonenumber=getphone).to_json())
            raise HTTPException(
                status_code=400, detail="account already exist..")
        except Account.DoesNotExist:
            hashPass = auth_handler.get_password_hash(details.password)
            getDetails = Account(phonenumber=getphone,
                                 password=hashPass)
            getDetails.save()
            token = auth_handler.encode_token(getphone)
            return {"message": "account created...", "token": token}

    except Signupauth.DoesNotExist:
        raise HTTPException(
            status_code=400, detail="invalid authcode..")
