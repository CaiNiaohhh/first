import sys, time, json
sys.path.append('..')
import Request

from flask import Flask, url_for, request
app = Flask(__name__)
@app.route('/', methods=['GET']) # 如果没有methods参数，默认只支持get,必须大写
def http_test():
    N = int(request.args.get("N"))
    L = int(request.args.get("L"))
    SNR = float(request.args.get("SNR"))
    bec_err = float(request.args.get("bec_err"))
    init_value = float(request.args.get("init_value"))
    channel = request.args.get("channel")
    algorithm = request.args.get("algorithm")

    print("N:", N)
    print("L:", L)
    print("SNR:", SNR)
    print("bec_err:", bec_err)
    print("init_value:", init_value)
    print("channel:", channel)
    print("algorithm:", algorithm)
    res = None
    # 当信道类型是BEC&&译码算法是SC
    if channel == "BEC" and algorithm == "SC":
        res = Request.BEC_SC(N, init_value, bec_err)
    # 当信道类型是BEC&&译码算法是SCL
    if channel == "BEC" and algorithm == "SCL":
        res = Request.BEC_SCL(N, init_value, L, bec_err)
    # 当信道类型是AWGN&&译码算法是SC
    if channel == "AWGN" and algorithm == "SC":
        res = Request.AWGN_SC(N, init_value, SNR)
    # 当信道类型是AWGN&&译码算法是SCL
    if channel == "AWGN" and algorithm == "SCL":
        res = Request.AWGN_SCL(N, init_value, SNR, L)
    return res

if __name__ == "__main__":
    app.run(host='0.0.0.0')


    
