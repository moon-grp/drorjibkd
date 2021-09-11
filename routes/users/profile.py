
from datetime import datetime, timedelta
from model.superadmin import Signupauth
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from warnings import catch_warnings
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from pydantic.networks import EmailStr
from model.users.profile import Profile
import json
from bson.objectid import ObjectId
from pydantic import BaseModel
from model.users.createacc import Account
from model.users.medicalcard import Card
from model.superadmin import Signupauth
import os
from passlib.context import CryptContext
from dotenv import load_dotenv
import validators
from config.userauth import AuthHandler
load_dotenv()


profile = APIRouter()
auth_handler = AuthHandler()


class Newaccount(BaseModel):
    firstname: str
    lastname: str
    gender: str
    dob:str
    address: str



@profile.post("/profile/create/{phn}", tags=["users"])
async def create_profile(details:Newaccount, phn):
    add_profile_details= Profile(
        firstname = details.firstname,
        lastname = details.lastname,
        gender = details.gender,
        dob = details.dob,
        address = details.address,
        phonenumber = phn
    )
    add_profile_details.save()
    return{
        "message": "Profile created..."
    }

@profile.get("/profile/getall", tags=["admin"])
async def get_all_profile():
    get_all = Profile.objects().to_json()
    fget_all = json.loads(get_all)
    return{
        "data": fget_all
    }
    

@profile.get("/profile/get/{phn}", tags=["admin"])
async def get_profile(phn):
    getProfile = Profile.objects(phonenumber=phn).to_json()
    fgetProile = json.loads(getProfile)
    return{
        "data": fgetProile
    }

