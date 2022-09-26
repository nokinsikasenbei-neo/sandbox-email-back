from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
# from pydantic import BaseModel
from typing import List

app = FastAPI()

"""
サンドボックス環境で添付ファイルを展開する
"""
def sandbox():
    return "ok"

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
    return JSONResponse(status_code=200)

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