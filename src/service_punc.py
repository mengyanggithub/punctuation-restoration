from service import app, process_request
from service_utils_punc import punc_restore


@app.post("/punc/predict")
async def predict_punc(request):
    return process_request(request, ["query"], punc_restore)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8501, debug=False, access_log=False)