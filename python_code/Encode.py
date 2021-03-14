from cal_bz import cal_z
from cal_GN import cal_GN
import numpy
import numpy as np

def Polar_Encode(valid_msg, N, K, init_value = 0.5):

    message = [0] * N # 默认冻结比特位为0
    # 先根据巴氏参数进行排序
    Bz_list = [[i, 0] for i in range(N)]
    for i in range(N):
        Bz_list[i][1] = cal_z(i, N, init_value)
    # 根据第二个数据进行排序
    res_list = sorted(Bz_list,key=lambda x:(x[1],x[0]))
    valid_index_list = [] # 挑选出有效位的下标
    for i in range(K):
        valid_index_list.append(res_list[i][0])
    valid_index_list.sort()
    for index in valid_index_list:
        message[index] = valid_msg.pop()
    # 计算转换矩阵GN
    GN = cal_GN(N)
    send_message = numpy.dot(message, GN) % 2
    # print(message, send_message)
    #　处理send_message
    y_tmp = np.array(send_message)
    y_tmp_tmp = []
    for y in y_tmp[0]:
        y_tmp_tmp.append(int(y))
    send_message = y_tmp_tmp
    return valid_index_list, message, send_message
