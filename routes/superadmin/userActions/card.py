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
import string
import random
from mongoengine.queryset.visitor import Q


cardops = APIRouter()

class cons_details(BaseModel):
    date: str
    cx: str
    dx: str
    invx: str
    rx: str

class cons_id(BaseModel):
    doc_id: str

class cons_update(BaseModel):
    doc_id: str
    date: str
    cx: str
    dx: str
    invx: str
    rx: str



@cardops.post("/createconsultation/{phn}", tags=["admin"])
async def create_consultation(details: cons_details, phn):
    chrset = ''
    chrset += string.ascii_letters
    doc_id = ''.join(random.choice(chrset) for i in range(5))
    patient= Card.objects.get(phonenumber=phn)
    consult = Consultations(date=details.date, cx=details.cx, dx=details.dx,invx=details.invx, rx=details.rx, doc_id=doc_id)
   # cons =[consult]
    cons = {
        "date":details.date,
        "cx": details.cx,
        "dx": details.dx,
        "invx": details.invx,
        "rx": details.rx,
        "doc_id": doc_id
    }
    patient.data2["consult"][doc_id]=cons
    patient.save()
    return{
        "message": "consultation recorded..."
    }

@cardops.get("/getconsultations/{phn}", tags=["admin"])
async def get_consultations(phn):
    get_record = Card.objects.get(phonenumber=phn).to_json()
    all_cons = json.loads(get_record)
    return  {
        "data": all_cons["data"]
    }

@cardops.get("/getconsultation/{phn}", tags=["admin"])
async def get_consultation(phn, details:cons_id):
    id= details.doc_id
    get_record = Card.objects.get(phonenumber=phn).to_json()
    u= json.loads(get_record)
    result = u["data2"]["consult"][id]
    return{
        "data": result
    }
   
@cardops.post("/updateconsultation/{phn}", tags=["admin"])
async def update_consultation(phn, details: cons_update):
    id= details.doc_id
    get_record = Card.objects.get(phonenumber=phn)
    cons = {
        "date":details.date,
        "cx": details.cx,
        "dx": details.dx,
        "invx": details.invx,
        "rx": details.rx,
        "doc_id": id
    }
    get_record.data2["consult"][id]=cons
    get_record.save()
    return{
       "message": "consultation record updated..."}


   
@cardops.delete("/deleteconsultation/{phn}", tags=["admin"])
async def update_consultation(phn, details: cons_id):
    id= details.doc_id
    get_record = Card.objects.get(phonenumber=phn)
    get_record.data2["consult"][id]={}
    get_record.save()
    return{
       "message": "consultation deleted..."}
