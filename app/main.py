from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from gmail import get_service, get_message_list, get_message

# from pydantic import BaseModel
import requests
from typing import List

app = FastAPI()

SANDBOX_ENDPOINT = 'http://sandbox:9000/convert'

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
        attachment = message.get('attachment')
        if attachment != '':
            res = requests.post(SANDBOX_ENDPOINT, json={'filename': attachment}) # sandbox環境にファイルのコンパートをリクエスト
            if res.status_code != 200:
                return JSONResponse(status_code=500, content={'error': 'internal server error.'})
        idx = attachment.find('.')
        if idx == -1:
            message['converted'] = ''
        else:
            message['converted'] = attachment.replace(attachment[idx:], '.pdf')
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