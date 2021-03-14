import math, numpy, random, copy
from SGA import SGA
from cal_GN import cal_GN
from AWGN_py import awgn
from Error_Bits import error_bits

# 高斯信道的编码格式
# 同样是假设冻结位比特全为0，有效信息位为1的情况
# 接受参数1、N: 信息总长度
# 2、init_value: 编码的准确率
# 3、SNR: 信噪比dB
def encode(valid_msg, N, init_value, SNR):
    num = 1
    K = int(N * init_value)
    snr = 10 ** (SNR / 10)
    p = math.sqrt(1/snr)
    variance = 1 / snr
    n = int(math.log2(N))

    LLR = [[0] * N for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(N):
            LLR[i][j] = [0, i, j]

    for i in range(len(LLR[0])):
        LLR[0][i][0] = 2 / variance

    for i in range(1, n + 1):
        for j in range(N):
            if j % 2 == 0:
                LLR[i][j][0] = SGA(LLR[i - 1][(j + 1) // 2][0])
            else:
                LLR[i][j][0] = 2*LLR[i - 1][j // 2][0]

    I = sorted(LLR[n],key=lambda x:(x[1],x[0]), reverse=True)
    UI = I[:K]
    valid_index_list = []
    for u in UI:
        valid_index_list.append(u[-1])
    valid_index_list.sort()
    X = [[0] * N for _ in range(num)]
    for i in range(num):
        for j in range(K):
            X[i][UI[j][2]] = valid_msg.pop()
    GN = cal_GN(N)
    send_message = numpy.dot(X, GN) % 2
    send_message = numpy.array(send_message)
    send_message = send_message[0]
    tmp = []
    for s in send_message:
        tmp.append(1-2*s)
    send_message = copy.copy(tmp)
    # print("未加噪声: ", send_message)
    # err_list = error_bits(N, K)
    for i in range(len(send_message)):
        # if i in err_list:
        guass = random.gauss(0, p)
        send_message[i] += guass
    for i in range(len(send_message)):
        send_message[i] = format(send_message[i], '.2f')
    # print("加完噪声: ", send_message)
    return valid_index_list, X[0], tmp, send_message, variance


#
# if __name__ == "__main__":
#     N = 8
#     init_value = 0.5
#     SNR = 2
#     encode(N, init_value, SNR)