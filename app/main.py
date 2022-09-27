from webbrowser import get
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
# from pydantic import BaseModel
from typing import List
import os.path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

app = FastAPI()
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

"""
サンドボックス環境で添付ファイルを展開する
"""
def sandbox():
    return "ok"

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
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=8001)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        service = build('gmail', 'v1', credentials=creds)
        return service
    except Exception as e:
        print(e)
        return None

"""
gmail apiを用いてメールを一括取得
"""
def get_mesage_list(service, user_id: str = 'me'):
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
        return messages
    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

@app.post("/authorize", tags=['Get Messages List'])
def authorize():
    service = get_service()
    if service != None:
        return JSONResponse(status_code=200)
    else:
        return JSONResponse(status_code=500)

@app.get("/messages", tags=['Get Messages List'])
def receive_email():
    """
    Get Messages List
    
    Request Params
    - None
    
    Response Params
    
    以下のリスト
    - raw: base64エンコードしたメールオブジェクト
    - file: 添付ファイル
    
    """
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            return JSONResponse(status_code=400, content={'message': 'log in first.'})
    
    try:
        service = get_service()
        messages = get_mesage_list(service)
        response_json = {"messages": messages}
        return JSONResponse(status_code=200, content=response_json)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500)

@app.post("/messages/send", tags=['Send Message'])
def send_email(raw: str, file: UploadFile = File(...)):
    """
    Send Message
    
    Request Params
    - raw: base64エンコードしたメールオブジェクト
    - file: 添付ファイル
    
    Response Params
    - None
    
    """
    return JSONResponse(status_code=200)