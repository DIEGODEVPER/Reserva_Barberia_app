from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime

class GoogleCalendar:
    def __init__(self, credentials_file,calendarid):
        self.credentials_file = credentials_file
        self.calendarid = calendarid
        self.service = self._create_service()

    def _create_service(self):
        credentials = service_account.Credentials.from_service_account_file(self.credentials_file, scopes=['https://www.googleapis.com/auth/calendar'])
        service = build('calendar', 'v3', credentials=credentials)
        return service

    def get_events(self, date=None): 
        # Obtener eventos
        if not date:
            events = self.service.events().list(calendarId=self.calendarid).execute()
        else:
            start_date = f"{date}T00:00:00Z"
            end_date = f"{date}T23:59:59Z"
            events = self.service.events().list(calendarId=self.calendarid, timeMin=start_date, timeMax=end_date).execute()
        return events.get('items', [])
    
    #get events by date and return the event id
    def get_event_by_date(self, start_date, end_date):
        # Obtener evento
        event= self.service.events().list(calendarId=self.calendarid, timeMin=start_date, timeMax=end_date).execute()
        #devolver el id del evento
        return event["items"][0]["id"]
    

    #def get_start_times(self, date):
        #events = self.get_events(date)
        #start_times = []  #Declaracion de la lista #para mi Yo del futuro, esta parte queda por pasar el contenido del diccionario a la lista creada
        #for event in events:
        #for x in events:
            #start_time = event['start']  #['dateTime']
            # parsed_start_time = datetime.fromisoformat(start_time[:-6])
           #hours_minutes = parsed_start_time.strftime("%H:%M")
           #start_times.append(hours_minutes)
           #start_time.append()
           #start_times.append(x[0]["start"]["dateTime"])
        #return start_time

    
    def create_event(self, name_event, start_time, end_time, timezone, attendees=None):
        # Crear un evento
        event = {
            'summary': name_event,
            'start': {
                'dateTime': start_time,
                'timeZone': timezone,
            },
            'end': {
                'dateTime': end_time,
                'timeZone': timezone,
            },
        }
        if attendees:
            event["attendees"] = [{"email": email} for email in attendees]

        try:
            created_event = self.service.events().insert(calendarId=self.calendarid, body=event).execute()
        except HttpError as error:
            raise Exception(f"An error has occurred: {error}")

        return created_event

    def update_event(self, event_id, summary=None, start_time=None, end_time=None):
        # Actualizar un evento
        event = self.service.events().get(calendarId=self.calendarid, eventId=event_id).execute()

        if summary:
            event['summary'] = summary

        if start_time:
            event['start']['dateTime'] = start_time.strftime('%Y-%m-%dT%H:%M:%S')

        if end_time:
            event['end']['dateTime'] = end_time.strftime('%Y-%m-%dT%H:%M:%S')

        updated_event = self.service.events().update(calendarId=self.calendarid, eventId=event_id, body=event).execute()
        return updated_event

    def delete_event(self, event_id):
        # Eliminar un evento
        self.service.events().delete(calendarId=self.calendarid, eventId=event_id).execute()
        return True

#prueba
#credentials = 'test-calendar-420116-6df0ced01187.json'
#calendarid = 'diegofiis10@gmail.com'

#calendar = GoogleCalendar(credentials, calendarid)

#Crea Evento
#name_evento = 'Evento de prueba'
#start_date = '2024-04-13T11:30:00-05:00'
#end_date = '2024-04-13T12:00:00-05:00'
#timezone = 'America/Lima'
#event = calendar.get_start_times('2024-04-12')
#print(event)
#creamos el evento
#event = calendar.create_event(name_evento, start_date,end_date, timezone)
#print(event['summary'], event['id'])
#-->Evento de prueba  oips6o1a5ntij09s7vbcgkht9c

#actualizar evento
#id = 'oips6o1a5ntij09s7vbcgkht9c'
#name_event = 'Evento de prueba 2'

#calendar.update_event(id, name_event)

#Eliminar evento
#id = 'oips6o1a5ntij09s7vbcgkht9c'
#calendar.delete_event(id)

#Metodos de captura
#id = 'oips6o1a5ntij09s7vbcgkht9c'
#name_event = 'Evento de prueba'
#date = '2024-04-13'
#leer eventos
#eventos = calendar.get_start_times(str('2024-04-13'))
##print(date)
#print(eventos)