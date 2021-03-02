from __future__ import print_function
import datetime
import json
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.

def getCalendarData(seconds=3600):
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if  not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            #make request
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    today = datetime.datetime.today() - datetime.timedelta(seconds=3*3600) #to Moscow time
    now = today.isoformat() + 'Z' # 'Z' indicates UTC time
    finish = (today + datetime.timedelta(0, seconds)).isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        timeMax=finish, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    resSet = []
    i = 0
    for event in events:
        resSet.append({})
        resSet[i]['creator'] = event['creator']['email']#author of note
        resSet[i]['start'] = event['start']['dateTime']#time when clock rings
        resSet[i]['end'] = event['end']['dateTime']#time when clock stops
        resSet[i]['data'] = event['summary']#text of note
        i+=1
    return json.dumps(resSet)