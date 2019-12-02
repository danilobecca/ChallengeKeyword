
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import ConectorMysql
import datetime

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'

def main():
    
    #Valida si estan generadas las credenciales para la busqueda, en caso de que no, solicita volver a loguearse en el navegador.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    
    # Hago la busqueda para traer el listado de IDs de mails que cumplen con la query definida.
    results = service.users().messages().list(userId='me',q='DevOps').execute() # pylint: disable=E1101
    messages = results.get('messages', [])
      
    if not messages:
        print ("No hay mails que contengan la palabra buscada.")
    else:
        print ('Se encontraron los siguientes mails:')
        print ('IdMsg','Fecha','From','Subject')
        for message in messages:
        #A través de la lista de IDs obtenidos, busco los campos que necesito de cada mail encontrado.
            msg = service.users().messages().get(userId='me', id=message['id']).execute() # pylint: disable=E1101
            
            mresult = msg['payload'].get('headers',[])
            
            #Realizamos la conversion de epoch a date
            epoch = int(msg['internalDate'])/1000
            dateM = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')
        
            #Envia los datos del mail encontrado a la base de datos.
            ConectorMysql.generate(msg['id'],dateM,mresult[-6].get('value'),mresult[-3].get('value'))
                      
            #Muestra los valores del mail encontrado que se grabó en la base.
            print(msg['id'],dateM,mresult[-6].get('value'),mresult[-3].get('value'))


if __name__ == '__main__':
    main()


        