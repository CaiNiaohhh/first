import numpy, math, copy
import numpy as np
from BAWGNC_Encode import encode

def cal_llr(i, N, y_msg, u_msg, u):
    if N == 1:
        llr = (2 * float(y_msg[0])) / u
    else:
        if i % 2 == 0:
            llr_1 = cal_llr(i // 2,
                            N // 2,
                            y_msg[:(N // 2)],
                            (u_msg[::2] ^ u_msg[1::2])[:(i // 2)], u)
            llr_2 = cal_llr(i // 2,
                            N // 2,
                            y_msg[N // 2:],
                            u_msg[1::2][:(i // 2)], u)
            p1 = math.exp(llr_1 + llr_2) + 1
            p2 = math.exp(llr_1) + math.exp(llr_2)
            llr = math.log(p1 / p2)

        else:
            llr_1 = cal_llr((i - 1) // 2,
                            N // 2,
                            y_msg[:(N // 2)],
                            (u_msg[:-1:2] ^ u_msg[1:-1:2])[:((i - 1) // 2)], u)
            llr_2 = cal_llr((i - 1) // 2,
                            N // 2,
                            y_msg[N // 2:],
                            u_msg[1::2][:((i - 1) // 2)], u)
            llr = llr_2 + ((-1) ** u_msg[-1]) * llr_1
    return float(llr)

def Polar_Decode(valid_index_list, N, y_msg, u):
    u_msg = numpy.zeros(N, dtype='uint8')  # 保存计算结果
    for index in valid_index_list:
        llr = cal_llr(index, N, y_msg, u_msg[:index], u)
        # print("llr:", llr)
        u_msg[index] = 0 if llr >= 0 else 1
        # print(index, ":", u_msg[index])
    # print(u_msg)
    return u_msg



def campare_bit(x):
    sign = -1 if x <= 0 else 1
    res = (1 - sign) // 2
    return res

def cal_PM(i, valid_index_list, llr, u, PM):
    PM[0] = PM[0] + str(u)
    x = campare_bit(llr)
    # 当i是冻结比特的时候
    if i not in valid_index_list:
        if u != 0:
            PM[1] = float("inf") # 表示无限大
            return
        else:
            if x != u:
                PM[1] += math.fabs(llr)
    else:
        if x != u:
            PM[1] += math.fabs(llr)


def AWGN_SCL_Decode(L, valid_index_list, N, y_msg, u):
    cnt = 1
    PM = [["", 0] for _ in range(L*L+1)]
    for i in range(N):
        # print(PM)
        u_msg = []
        if i == 0:
            u_msg.append(np.zeros(0, dtype='uint8'))
        else:
            for P in PM:
                if P[0] != "":
                    tmp = np.zeros(len(P[0]), dtype='uint8')
                    for p in range(len(P[0])):
                        tmp[p] = P[0][p]
                    u_msg.append(tmp)

        for j in range(cnt):
            llr = cal_llr(i, N, y_msg, u_msg[j][:i], u)
            llr = float(format(llr, ".2f"))
            PM[j + cnt] = copy.copy(PM[j])
            cal_PM(i, valid_index_list, llr, 0, PM[j])
            cal_PM(i, valid_index_list, llr, 1, PM[j + cnt])
        cnt *= 2
        if cnt <= L:
            continue
        PM = sorted(PM, key=lambda x: (x[1], x[0]))
        count = 0
        for p in PM:
            if p[0] == "":
                count += 1
        PM = PM[count:]
        for _ in range(count):
            PM.append(['', 0])
        cnt //= 2
    # print(PM)
    return list(PM[0][0])


if __name__ == "__main__":
    print("running...")

    N = 128
    L = 4
    # X表示编码前的信息， y_msg表示接收到的信息
    init_value, SNR = 1, 1.3
    valid_index_list, X, _, y_msg, u = encode([1, 0, 1] * N, N, init_value, SNR)
    l1 = AWGN_SCL_Decode(1, valid_index_list, N, y_msg, u)
    lL = AWGN_SCL_Decode(L, valid_index_list, N, y_msg, u)
    # l2 = Polar_Decode(valid_index_list, N, y_msg)
    # for i in range(N):
    #     if int(X[i]) != int(l1[i]) or int(X[i]) != int(l2[i]):
    #         for j in range(N):
    #             if int(l2[i]) != int(l1[i]):
    #                 print("X:", X)
    #                 print("l1:", l1)
    #                 print("l2:", l2)
    #         break

