import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
FILE_STORAGE = '/var/public/attached/'

"""
gmail apiを使用するためのserviceインスタンスを作成
"""
def get_service():
    creds = None
    service = None
    try:
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                return None
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(e)
        return None


"""
gmail apiを用いてメールを一括取得
"""
def get_message_list(service, user_id: str = 'me'):
    messages = []
    try:
        # Call the Gmail API
        message_ids = service.users().messages().list(userId=user_id).execute()
        for message_id in message_ids["messages"]:
            message = {}
            message['id'] = message_id['id']
            message_detail = service.users().messages().get(userId=user_id, id=message_id["id"]).execute()
            headers = message_detail['payload']['headers']
            
            for d in headers:
                if d['name'] == 'Subject':
                    message['subject'] = d['value']
                if d['name'] == 'From':
                    message['from'] = d['value']
                    
            message['body'] = ""
            message['attachment'] = ""
            
            if message_detail['payload'].get('parts') != None:
                for part in message_detail['payload']['parts']:
                    # ファイルが添付されている場合の処理
                    if part['filename']:
                        message['attachment'] = part['filename']
                        if 'data' in part['body']:
                            data=part['body']['data']
                        else:
                            att_id=part['body']['attachmentId']
                            att=service.users().messages().attachments().get(userId=user_id, messageId=message_id,id=att_id).execute()
                            data=att['data']
                        file_data = base64.urlsafe_b64decode(data.encode('utf-8'))
                        path = FILE_STORAGE + part['filename']
                        
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
            
            else:
                if 'data' in  message_detail['payload']['body']:
                    decoded_bytes = base64.urlsafe_b64decode(
                        message_detail['payload']['body']['data'])
                    decoded_message = decoded_bytes.decode('utf-8')
                    message['body'] += decoded_message
            messages.append(message)
        return messages
    except Exception as e:
        print(f'An error occurred: {e}')
        return e
