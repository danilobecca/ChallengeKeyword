import peewee 
from peewee import *
import database


def save(customID,customDate,customFrom,customSub):
    
    try:
            mail = DataMail.get(DataMail.idMail == customID)
    except DataMail.DoesNotExist:
            mail = DataMail.insert(
            idMail=customID,
            dateMsg=customDate,
            fromMsg=customFrom,
            subjectMsg=customSub)