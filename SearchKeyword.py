
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import ConectorMysql
import datetime

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
#SCOPES = ['https://mail.google.com/']



def main():
    
    #Valida si estan generadas las credenciales, en caso de que no, solicita volver a loguearse en el navegador.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    
    # Hago la busqueda para traer un listado de IDs de mails que cumplen con la query definida.
    try:
        results = service.users().messages().list(userId='me',q='DevOps').execute() # pylint: disable=E1101
        messages = results.get('messages', [])
      
        #A través de la lista de IDs obtenidos, busco los campos que necesito de cada mail encontrado.
        print ('Se encontraron los siguientes mails:')
        print ('IdMsg','Fecha','From','Subject')
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute() # pylint: disable=E1101
     
            #print ('msg id: %s - msg internalDate: %s' % (msg['id'], msg['internalDate']))
            mresult = msg['payload'].get('headers',[])
            
            #Realizamos la conversion de epoch a date
            epoch = int(msg['internalDate'])/1000
            dateM = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')
        
            #Enviamos los datos a la base de datos.
            ConectorMysql.save(msg['id'],dateM,mresult[-6].get('value'),mresult[-3].get('value'))       
            
            #Mostramos los valores que se enviaron a la base de datos.
            print(msg['id'],dateM,mresult[-6].get('value'),mresult[-3].get('value'))
    except Exception as e:
        print(f'No hay mensajes que cumplan el criterio de busqueda: {e}')

if __name__ == '__main__':
    main()


        