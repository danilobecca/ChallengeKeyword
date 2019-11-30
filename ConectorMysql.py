import peewee 
from peewee import *
import datetime

#Conexión con nuestra base de datos.
db = MySQLDatabase('keyword', user='root',passwd='root.2019')

#Definición de la clase DataMail, la cual utilizaremos para insertar en la base de datos.
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
            mail = DataMail.create(
            idMail=customID,
            dateMsg=customDate,
            fromMsg=customFrom,
            subjectMsg=customSub)
