from __future__ import print_function
import pickle
import os.path
from get_message_info import get_message_info
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText
import time
from history_last_handler import *
from get_messages_api import get_new_messages, Message
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from send_message_api import *
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def cannary(service):
    message = MIMEText("Всё в порядке")
    message['to'] = 'futureinrevolution@gmail.com'
    message['from'] = 'knmatmeh@gmail.com'
    message['subject'] = "Отчёт"
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    try:
        message = (service.users().messages().send(userId="me", body={
        'raw': raw_message.decode("utf-8")
    })
                   .execute())
        print('Message Id: %s' % message['id'])
        return message
    # except errors.HttpError, error:
    except:
        print('An error occurred: %s')

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    mail = ""
    with open("mails", "r") as fp:
        mail = str(fp.read())
    service = build('gmail', 'v1', credentials=creds)
    mail = "futureinrevolution@gmail.com, oleg.belohohlov01@gmail.com, inhelsmith@gmail.com"
    history_last = read_history_last()
    count = 0
    while(True):
        if count % 120 == 0:
            count = 0
            cannary(service)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        messages = get_new_messages(history_last,service)
        write_history_last(messages[1])
        history_last = messages[1]
        print(count)
        for msg in messages[0]:
            print(history_last)
            print(messages[0])
            send_message_brief(mail, msg, service)
        time.sleep(10)
        count += 1


if __name__ == '__main__':
    main()
