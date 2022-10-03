from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from gmail import get_service, get_message_list, get_message

# from pydantic import BaseModel
import requests
import re
from typing import List

app = FastAPI()

SANDBOX_ENDPOINT = 'http://sandbox:9000/convert'
URL_ENDPOINT = 'http://url:10000/url'

@app.get("/messages", tags=['Get Messages List'])
def messages():
    try:
        service = get_service()
        if service == None:
            return JSONResponse(status_code=400, content={'error': 'please issue oauth token.'})
        messages = get_message_list(service)
        response_json = {"messages": messages}
        return JSONResponse(status_code=200, content=response_json)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={'error': 'internal server error.'})

@app.get("/message/{msg_id}", tags=['Get Message'])
def message(msg_id: str):
    try:
        service = get_service()
        if service == None:
            return JSONResponse(status_code=400, content={'error': 'please issue oauth token.'})
        message = get_message(service, msg_id)
        # 添付ファイルの変換
        attachment = message.get('attachment')
        if attachment != '' and attachment != None:
            res = requests.post(SANDBOX_ENDPOINT, json={'filename': attachment}) # sandbox環境にファイルのコンパートをリクエスト
            if res.status_code != 200:
                return JSONResponse(status_code=500, content={'error': 'internal server error.'})
        idx = attachment.find('.')
        if idx == -1:
            message['converted'] = ''
        else:
            message['converted'] = attachment.replace(attachment[idx:], '.pdf')
            
        # URLの判定
        body = message['body']
        http_pattern = "http?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        https_pattern = "https?://[\w/:%#\$&\?\(\)~\.=\+\-]+"
        http_url_list = re.findall(http_pattern, body)
        https_url_list = re.findall(https_pattern, body)
        url_list = http_url_list + https_url_list
        message['url_list'] = url_list
        
        results = []
        if len(url_list) > 0:
            res = requests.post(URL_ENDPOINT, json={'url_list': url_list})
            results = res.json()['results']
        message['results'] = results
        
        response_json = {"message": message}
        return JSONResponse(status_code=200, content=response_json)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={'message': 'internal server error.'})

@app.get("/file", tags=['Get File'])
def file(name: str):
    # filename validation
    for char in name:
        if (char.isalnum() == False) and (char != '.'):
            return JSONResponse(status_code=400, content={'error': 'invalid request.'})
    return FileResponse(path=f"/var/public/converted/{name}")

@app.post("/messages/send", tags=['Send Message'])
def send_email(raw: str, file: UploadFile = File(...)):
    return JSONResponse(status_code=200)