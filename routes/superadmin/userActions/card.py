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
from model.users.medicalcard import Card
from model.users.medicalcard import Consultations


cardops = APIRouter()

class cons_details(BaseModel):
    date: str
    cx: str
    dx: str
    invx: str
    rx: str


@cardops.post("/createconsultation/{phn}", tags=["admin"])
async def create_consultation(details: cons_details, phn):
    patient= Card.objects.get(phonenumber=phn)
    consult = Consultations(date=details.date, cx=details.cx, dx=details.dx,invx=details.invx, rx=details.rx)
    cons =[consult]
    patient.data.append(cons)
    patient.save()
    return{
        "message": "consultation recorded..."
    }


