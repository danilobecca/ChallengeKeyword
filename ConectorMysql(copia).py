import peewee 
from peewee import *
import datetime



db = MySQLDatabase('keyword', user='root',passwd='root.2019')

class DataMail(peewee.Model):
    idMail = peewee.TextField(default='')
    dateMsg = peewee.DateField(default=datetime.datetime.now)
    fromMsg = peewee.TextField(default='')
    subjectMsg = peewee.TextField(default='')

    class Meta:
        database = db


#Metodo para grabar los resultado en la BD, validando previamente si existe o no el ID del mail.

def save(customID,customDate,customFrom,customSub):

    
    try:
            mail = DataMail.get(DataMail.idMail == customID)
    except DataMail.DoesNotExist:
            mail = DataMail.insert(
            idMail=customID,
            dateMsg=customDate,
            fromMsg=customFrom,
            subjectMsg=customSub)

    
   # DataMail.insert()
    #mail = DataMail(idMail=customID,dateMsg=customDate,fromMsg=customFrom,subjectMsg=customSub)
    #mail.save()



#def getAll():
 #   for mail in DataMail.select():
  #      print (mail.idMail)
