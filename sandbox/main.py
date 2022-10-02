import json
from flask import Flask, request, Response

app = Flask(__name__)

@app.get("/")
def index():
    return "ok"

@app.post("/convert")
def convert():
    try:
        data = request.get_json()
        filename = data.get("filename")
        for char in filename:
            if not char.isalnum():
                return Response(response=json.dumps({'error': 'invalid request'}), status=400)
        exec(f"libreoffice7.3 --headless --convert-to pdf:writer_pdf_Export --outdir /var/public/converted /var/public/attached/{filename}")
    except Exception as e:
        print('error:', e)
        return Response(response=json.dumps({'error': 'internal server error'}), status=500)
    return Response(status=200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)