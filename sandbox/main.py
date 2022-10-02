import os
from flask import Flask, url_for, request

app = Flask(__name__)

@app.get("/")
def index():
    return "ok"

@app.post("/convert")
def convert():
    data = request.get_json()
    filename = data.get("filename")
    for char in filename:
        if not char.isalnum():
            return "false"
    exec(f"libreoffice7.3 --headless --convert-to pdf:writer_pdf_Export /sandbox/{filename}")
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)