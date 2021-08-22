from fastapi import APIRouter, File, UploadFile, Form, Depends, HTTPException
from mongoengine import signals
from model.superadmin import Signupauth
import json
from bson.objectid import ObjectId
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import string
import random


supadmin = APIRouter()


class gencode(BaseModel):
    phonenumber: str


@supadmin.post("/generatecode", tags=["admin"])
async def gen_code(details: gencode):
    if len(details.phonenumber) > 11 or len(details.phonenumber) < 11:
        raise HTTPException(
            status_code=400, detail="phone number longer or shorter than 11..")
    else:
        try:
            checkE = json.loads(Signupauth.objects.get(
                phonenumber=details.phonenumber).to_json())
            raise HTTPException(
                status_code=400, detail="phone number already exist..")
        except Signupauth.DoesNotExist:
            phonenumber = details.phonenumber
            chrset = ''
            chrset += string.ascii_letters
            signupCode = ''.join(random.choice(chrset) for i in range(10))
            new = Signupauth(phonenumber=phonenumber, authcode=signupCode)
            new.save()
            return{"phonenumber": details.phonenumber, "code": signupCode}


@supadmin.get("/getallcodes", tags=["admin"])
async def get_code():
    getcodes = Signupauth.objects().to_json()
    fmtCodes = json.loads(getcodes)
    return {"results": fmtCodes}


@supadmin.get("/searchcodes/{phn}", tags=["admin"])
async def search_code(phn):
    if len(phn) > 11 or len(phn) < 11:
        raise HTTPException(
            status_code=400, detail="phone number longer or shorter than 11..")
    else:
        try:
            prod = Signupauth.objects.get(phonenumber=phn)
            get_details = {
            "code":prod.authcode
            }
            return get_details
        except Signupauth.DoesNotExist:
            raise HTTPException(status_code=400, detail="Phone number does not exist")


@supadmin.delete("/deletecodes/{phn}", tags=["admin"])
async def delete_code(phn):
    if len(phn) > 11 or len(phn) < 11:
        raise HTTPException(
            status_code=400, detail="phone number longer or shorter than 11..")
    else:
        try:
            prod = Signupauth.objects.get(phonenumber=phn)
            prod.delete()
            return{"message":"phonenumber and code deleted"}
        except Signupauth.DoesNotExist:
            raise HTTPException(status_code=400, detail="Phone number does not exist")


