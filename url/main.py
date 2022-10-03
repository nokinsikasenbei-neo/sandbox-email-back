import json
from flask import Flask, request, Response
from deturl import urldet


app = Flask(__name__)

@app.get("/")
def index():
    return "ok"

@app.post("/url")
def url():
    try:
        data = request.get_json()
        url_list = data.get("url_list")
        print('url_list:', url_list)

        results = []
        for url in url_list:
            result = urldet(url)
            results.append(result)
        print('results:', results)
        return Response(response=json.dumps({'results': results}), status=200)
    except Exception as e:
        print('error:', e)
        return Response(response=json.dumps({'error': 'internal server error'}), status=500)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)