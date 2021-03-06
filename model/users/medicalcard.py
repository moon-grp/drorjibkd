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
    doc_id = StringField()


class Card(Document):
    #data= DictField(EmbeddedDocumentListField(Consultations))
    data = ListField()
    data2 = DictField()
    phonenumber = StringField(max_length=11)
    