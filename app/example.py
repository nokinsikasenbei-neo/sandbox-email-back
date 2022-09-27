from __future__ import print_function
from email import message

import os.path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def decode_base64url_data(data):
    """
    base64url のデコード
    """
    decoded_bytes = base64.urlsafe_b64decode(data)
    decoded_message = decoded_bytes.decode("UTF-8")
    return decoded_message

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # creds = flow.run_console()
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    messages = []
    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        messages = []
        message_ids = service.users().messages().list(userId='me').execute()
        for message_id in message_ids["messages"]:
            message = {}
            print(message_id)
            message['id'] = message_id['id']
            message_detail = service.users().messages().get(userId="me", id=message_id["id"]).execute()
            headers = message_detail['payload']['headers']
            
            for d in headers:
                if d['name'] == 'Subject':
                    message['subject'] = d['value']
                if d['name'] == 'From':
                    message['from'] = d['value']
                    
            message['body'] = ""
            message['attachment'] = ""
            for part in message_detail['payload']['parts']:
                # ファイルが添付されている場合の処理
                if part['filename']:
                    message['attachment'] = part['filename']
                    if 'data' in part['body']:
                        data=part['body']['data']
                    else:
                        att_id=part['body']['attachmentId']
                        att=service.users().messages().attachments().get(userId="me", messageId=message_id,id=att_id).execute()
                        data=att['data']
                    file_data = base64.urlsafe_b64decode(data.encode('utf-8'))
                    # print(file_data.decode('utf-8'))
                    path = part['filename']
                    
                    with open(path, 'wb') as f:
                        f.write(file_data)
             
                if part['mimeType'] == 'multipart/alternative':
                    for ppart in part['parts']:
                        if 'data' in ppart['body']:
                            decoded_bytes = base64.urlsafe_b64decode(
                                ppart['body']['data'])
                            decoded_message = decoded_bytes.decode('utf-8')
                            message['body'] += decoded_message
                else:       
                    if 'data' in part['body']:
                        decoded_bytes = base64.urlsafe_b64decode(
                            part['body']['data'])
                        decoded_message = decoded_bytes.decode('utf-8')
                        message['body'] += decoded_message
            messages.append(message)
        print(messages)
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()