import peewee 
from peewee import *
import datetime


db = MySQLDatabase('keyword', user='root',passwd='root.2019')

class DataMail(peewee.Model):
    idMail = peewee.TextField(default='')
    dateMsg = peewee.TextField(default='')            #datetime.datetime.now)
    fromMsg = peewee.TextField(default='')
    subjectMsg = peewee.TextField(default='')

    class Meta:
        database = db

db.connect()
db.create_tables([DataMail], safe=True)