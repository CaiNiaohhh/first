N = 8 # 码长
K = 4 # 消息比特数

import numpy as np
# 计算巴氏参数
def cal_z(i, N, init_value = 0.5):
    if i == 0 and N == 1:
        return init_value
    else:
        if i % 2 == 0:
            return 2 * cal_z(i / 2, N / 2, init_value) - np.power(cal_z(i / 2, N / 2, init_value), 2)
        else:
            return np.power(cal_z((i - 1) / 2, N / 2, init_value), 2)

if __name__ == "__main__":
    for i in range(N):
        print(cal_z(i, N))