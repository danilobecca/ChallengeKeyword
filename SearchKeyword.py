
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import ConectorMysql
import datetime

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
#SCOPES = ['https://mail.google.com/']



def main():
   
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('gmail', 'v1', http=creds.authorize(Http()))
    
    # Hago la busqueda para traer los IDs de los que cumplan la query.
    results = service.users().messages().list(userId='me',q='DevOps').execute() # pylint: disable=E1101
    messages = results.get('messages', [])
    
    
    # Call the Gmail API to fetch INBOX
    #results = service.users().messages().list(userId='me',labelIds = ['INBOX']).execute() # pylint: disable=E1101
    #messages = results.get('messages', [])
    

    if not messages:
        print ("La bandeja esta vacia.")
    else:
        print ('Se encontraron los siguientes mails:')
        print ('IdMsg','Fecha','From','Subject')
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute() # pylint: disable=E1101
            
            #print ('msg id: %s - msg internalDate: %s' % (msg['id'], msg['internalDate']))
            mresult = msg['payload'].get('headers',[])
            
            #Realizamos la conversion de epoch a date
            epoch = int(msg['internalDate'])/1000
            dateM = datetime.datetime.fromtimestamp(epoch).strftime('%Y-%m-%d %H:%M:%S')
        
            #Este por ahora es el que funciona.
            ConectorMysql.save(msg['id'],dateM,mresult[-6].get('value'),mresult[-3].get('value'))
                      
            
            print(msg['id'],dateM,mresult[-6].get('value'),mresult[-3].get('value'))
            
            #-3 es el subject y -6 es el From
            #print(msg['id'])
            #print(epoch)
            #print(mresult[-6].get('value'))
            #print(mresult[-3].get('value'))
            
            
            
            
            #BUSCAR COMO VALIDAR sin repetir ID
            
            #ConectorMysql.save(msg['id'],convertDate,'BUSCARFROM',mresult[-3].get('value'))

            #ConectorMysql.getAll()



if __name__ == '__main__':
    main()


        