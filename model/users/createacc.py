from mongoengine import Document, StringField, DecimalField, URLField, BooleanField, ObjectIdField, EmailField, IntField, DateField
from dotenv import load_dotenv
from mongoengine import connect, disconnect
import os
load_dotenv()


uri = os.getenv("Mongo_db")

connect(host=uri, alias="default")


class Account(Document):
    password = StringField()
    phonenumber = StringField(max_length=11)
    