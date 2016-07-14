# -*- coding: utf-8 -*-
import os
import datetime
import time
import oauth2client
from oauth2client import client
from oauth2client import tools
from apiclient import discovery
import httplib2
import package_name.context as context

flags = None
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_id.json'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = context.APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def calender_check(calendar_id, find_str, date_str=time.strftime('%Y-%m-%d', datetime.datetime.now().timetuple())):
    check_bool = False
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    events_result = service.events().list(
        calendarId=calendar_id, timeMin=date_str + 'T00:00:00+09:00',
        # calendarId='primary', timeMin=now_str + 'T00:00:00+09:00',
        timeMax=date_str + 'T23:59:59+09:00', maxResults=1000, singleEvents=True,
        orderBy='startTime').execute()

    events = events_result.get('items', [])

    for event in events:
        if event['summary'].find(find_str) > -1:
            check_bool = True

    return check_bool
