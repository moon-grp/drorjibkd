from mongoengine import Document, StringField, DecimalField, URLField, BooleanField, ObjectIdField, EmailField, IntField, DateField, DictField, EmbeddedDocument, EmbeddedDocumentListField
from dotenv import load_dotenv
from mongoengine import connect, disconnect
import os

from mongoengine.fields import DictField, ListField
load_dotenv()


uri = os.getenv("Mongo_db")

connect(host=uri, alias="default")


class Consultations(EmbeddedDocument):
    date = StringField()
    cx = StringField()
    dx = StringField()
    invx = StringField()
    rx = StringField()


class Card(Document):
    data= ListField(EmbeddedDocumentListField(Consultations))
    phonenumber = StringField(max_length=11)
    