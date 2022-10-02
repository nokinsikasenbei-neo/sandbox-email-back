from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from gmail import get_service, get_message_list

# from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.get("/messages", tags=['Get Messages List'])
def get_messages():
    try:
        service = get_service()
        if service == None:
            return JSONResponse(status_code=400, content={'message': 'please issue oauth token.'})
        messages = get_message_list(service)
        response_json = {"messages": messages}
        return JSONResponse(status_code=200, content=response_json)
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': 'internal server error.'})

@app.get("/messages", tags=['Get Messages List'])
def get_message():
    try:
        service = get_service()
        if service == None:
            return JSONResponse(status_code=400, content={'message': 'please issue oauth token.'})
        messages = get_message_list(service)
        response_json = {"messages": messages}
        return JSONResponse(status_code=200, content=response_json)
    except Exception as e:
        return JSONResponse(status_code=500, content={'message': 'internal server error.'})

@app.post("/messages/send", tags=['Send Message'])
def send_email(raw: str, file: UploadFile = File(...)):
    return JSONResponse(status_code=200)