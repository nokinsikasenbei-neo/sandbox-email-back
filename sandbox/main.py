import json
import subprocess
from subprocess import PIPE
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
        print('filename:', filename)
        for char in filename:
            if (char.isalnum() == False) and (char != '.'):
                print("char:", char)
                return Response(response=json.dumps({'error': 'invalid request'}), status=400)
        cmd = "libreoffice7.3 --headless --convert-to pdf:writer_pdf_Export --outdir /var/public/converted /var/public/attached/%s" % filename
        proc = subprocess.run(cmd, shell=True, stdout=PIPE, stderr=PIPE, text=True)
        stdout = proc.stdout
        print('STDOUT: {}'.format(stdout))
    except Exception as e:
        print('error:', e)
        return Response(response=json.dumps({'error': 'internal server error'}), status=500)
    return Response(status=200)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9000, debug=True)