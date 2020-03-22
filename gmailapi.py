from __future__ import print_function
import pickle
import os.path
from base64 import urlsafe_b64encode
from email.mime.text import MIMEText
import time
from history_last_handler import *
from get_messages_api import get_new_messages
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from send_message_api import *
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

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
    send_to_mails = ["futureinrevolution@gmail.com"]
    service = build('gmail', 'v1', credentials=creds)
    history_last = read_history_last()
    while(True):
        messages = get_new_messages(history_last,service)
        write_history_last(messages[1])
        history_last = messages[1]
        print(messages[0])
        for msg in messages[0]:
            print(history_last)
            print(messages[0])
            for mail in send_to_mails:
                send_message_brief(mail, msg.text, service)
        time.sleep(15)


if __name__ == '__main__':
    main()
# [END gmail_quickstart]
