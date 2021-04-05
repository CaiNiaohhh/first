import math, copy, numpy
import numpy as np
import Encode, Error_Bits, cal_Bn

def cal_llr(i, N, y_msg, u_msg):
    if i == 0 and N == 1:
        if y_msg[i] == 1:
            llr = -10000
        elif y_msg[i] == 0:
            llr = 10000
        else:
            llr = 0
    else:
        if i % 2 == 0:
            llr_1 = cal_llr(i // 2,
                           N // 2,
                           y_msg[:(N // 2)],
                           (u_msg[::2] ^ u_msg[1::2])[:(i // 2)])
            llr_2 = cal_llr(i // 2,
                           N // 2,
                           y_msg[N // 2:],
                           u_msg[1::2][:(i // 2)])
            # print("   llr_1:", llr_1, "llr_2:", llr_2)
            # if llr_2 + llr_1 > 100:
            #     llr = 100
            # elif llr_1 > 100 or llr_2 > 100:
            #     llr = -100
            # else:
            #     p1 = math.exp(llr_1 + llr_2) + 1
            #     p2 = math.exp(llr_1) + math.exp(llr_2)
            #     if p2 == 0:
            #         llr = 100
            #     else:
            #         llr = math.log(p1 / p2)
            # p1 = math.exp(llr_1 + llr_2) + 1
            # p2 = math.exp(llr_1) + math.exp(llr_2)
            # llr = math.log(p1 / p2)
            if abs(llr_1) > 44 and abs(llr_2) > 44:
                if llr_1 * llr_2 > 0:
                    llr = min(abs(llr_1), abs(llr_2))
                else:
                    llr = -min(abs(llr_1), abs(llr_2))
            else:
                llr = 2 * np.arctanh(np.tanh(llr_1 / 2) * np.tanh(llr_2 / 2))


        else:
            llr_1 = cal_llr((i - 1) // 2,
                           N // 2,
                           y_msg[:(N // 2)],
                           (u_msg[:-1:2] ^ u_msg[1:-1:2])[:((i - 1) // 2)])
            llr_2 = cal_llr((i - 1) // 2,
                           N // 2,
                           y_msg[N // 2:],
                           u_msg[1::2][:((i - 1) // 2)])
            # print("llr_1:", llr_1, "llr_2:", llr_2)
            llr = llr_2 + ((-1) ** u_msg[-1]) * llr_1
    return float(llr)


def Polar_Decode(valid_index_list, N, y_msg, u_msg):
    for index in valid_index_list:
        llr = cal_llr(index, N, y_msg, u_msg[:index])
        # print("llr:", llr)
        u_msg[index] = 0 if llr >= 0 else 1
    return u_msg

def compare_bit(x):
    sign = -1 if x <= 0 else 1
    res = (1 - sign) // 2
    return res

def cal_PM(i, valid_index_list, llr, u, PM):
    PM[0] = PM[0] + str(u)
    x = compare_bit(llr)
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


def SCL_Decode(L, valid_index_list, N, y_msg):
    cnt = 1
    PM = [["", 0] for _ in range(L*L+1)]
    for i in range(N):
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
            llr = cal_llr(i, N, y_msg, u_msg[j][:i])
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

#
#
# if __name__ == "__main__":
#     N = 8
#     init_value = 0.5
#     K = int(N * init_value)  # 有效的码长
#     L = 8
#     # 判断SC译码和SCL的译码准确率
#     print("running...")
#     while True:
#         valid_msg = [1, 1] * N
#         u_msg = np.zeros(N, dtype='uint8')  # 保存计算结果
#         valid_index_list, u_message, y_message = Encode.Polar_Encode(valid_msg, N, K, init_value)
#         valid_index_list = [3, 5, 6, 7]
#         y_tmp = np.array(y_message)
#         y_tmp_tmp = []
#         for y in y_tmp[0]:
#             y_tmp_tmp.append(int(y))
#         y_message = y_tmp_tmp
#         # 假设传输过程中有N-K个比特出错
#         error_bit_list = Error_Bits.error_bits(N, K)
#         for err_bit in error_bit_list:
#             y_message[err_bit] = 2  # 设置为2表示传输过程中出错了
#         l1 = Polar_Decode(valid_index_list, N, y_message, u_msg)
#         l2 = SCL_Decode(L, valid_index_list, N, y_message)
#
#         for i in range(N):
#             if int(u_message[i]) != int(l1[i]) or int(u_message[i]) != int(l2[i]):
#                 for j in range(N):
#                     if int(l2[i]) != int(l1[i]):
#                         print("u_message:", u_message)
#                         print("l1:", l1)
#                         print("l2:", l2)
#                 break








