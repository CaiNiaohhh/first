'''
author: lrb
time: 2021-03-09
function: 实现不同编码不同译码算法的运行效率和译码准确性
          后期导入python的图表库 将结果可视化
'''
import Encode, Decode, BAWGNC_Encode, AWGN_Decode, Error_Bits
import numpy, math, copy
import numpy as np
import matplotlib.pyplot as plt
from timeit import default_timer as timer

'''
    假设填补的有效比特都为1,冻结比特都为0
'''

# 比较两个序列的相同位置比特相同的个数
def cmp_bits(l1, l2, valid_index_list):
    l = len(l1)
    cnt = 0
    for i in range(l):
        if i in valid_index_list and int(l1[i]) == int(l2[i]):
            cnt += 1
    return cnt

# 比较两个比特序列是否全等
def is_equal(l1, l2):
    l = len(l1)
    for i in range(l):
        if int(l1[i]) != int(l2[i]):
            print("NO index--->", i)
            exit("l1[i] != l2[i]")

'''
func:[BEC信道模型] 对比SC与SCL译码算法的运行时间
'''
def cmp_BEC_run_time(cnt, N, init_value, L):
    # t1, t2 分别表示SC, SCL的运行时间
    t1 = t2 = 0
    K = int(N * init_value)
    valid_msg = [1] * K
    valid_index_list, _, y_msg = Encode.Polar_Encode(valid_msg, N, K, init_value)
    # 假设传输过程中有N-K个比特出错
    error_bit_list = Error_Bits.error_bits(N, int(0.8*N))
    for err_bit in error_bit_list:
        y_msg[err_bit] = 2  # 设置为2表示传输过程中出错了
    # 计算SC运行所花费的时间
    start_time = timer()
    for _ in range(cnt):
        u_msg = np.zeros(N, dtype='uint8')  # 保存计算结果
        Decode.Polar_Decode(valid_index_list, N, y_msg, u_msg)
    end_time = timer()
    t1 = (end_time - start_time) / cnt
    print("N =", N, "K =", K, "的情况下\n SC译码所用时间为:", t1)

    # 计算SCL运行所花费的时间
    start_time = timer()
    for _ in range(cnt):
        Decode.SCL_Decode(L, valid_index_list, N, y_msg)
    end_time = timer()
    t2 = (end_time - start_time) / cnt
    print("N =", N, "K =", K, "L =", L, "的情况下\n SCL译码所用时间为:", t2)
    return t1, t2


'''
func:[BEC信道模型] 对比SC与SCL译码算法的译码准确性
'''
def cmp_BEC_correct(cnt, N, init_value, L):
    '''
        c1, c2 分别表示SC, SCL的译码准确率
        计算公式为 (cnt次译码过程中`所有译码正确的比特数量`) / int(N * init_value) * cnt
    '''
    c1 = c2 = 0
    K = int(N * init_value)
    for _ in range(cnt):
        valid_msg = [0,1] * K
        valid_index_list, o_msg, y_msg = Encode.Polar_Encode(valid_msg, N, K, init_value)
        # print("o_msg", o_msg)
        # print("y_msg", y_msg)
        # 假设传输过程中有BEC_Error*N个比特出错
        error_bit_list = Error_Bits.error_bits(N, int((1-BEC_Error)*N))
        for err_bit in error_bit_list:
            y_msg[err_bit] = 2  # 设置为2表示传输过程中出错了
        u_msg = np.zeros(N, dtype='uint8')  # 保存计算结果
        u_res = Decode.Polar_Decode(valid_index_list, N, y_msg, u_msg)
        u_scl_res = Decode.SCL_Decode(L, valid_index_list, N, y_msg)
        c1 += cmp_bits(o_msg, u_res, valid_index_list)
        c2 += cmp_bits(o_msg, u_scl_res, valid_index_list)
    c1 = c1 / (K * cnt)
    c2 = c2 / (K * cnt)
    print("N =", N, "K =", K, " 的情况下\n运行 ",cnt, "次,SC译码准确率为: ", c1)
    print("N =", N, "K =", K, "L =", L, " 的情况下\n运行 ",cnt, "次,SCL译码准确率为: ", c2)
    return c1, c2

'''
func:[AWGN信道模型] 对比SC与SCL译码算法的运行时间
'''

def cmp_AWGN_run_time(cnt, N, init_value, SNR, L):
    # t1, t2 分别表示SC, SCL的运行时间
    t1 = t2 = 0
    K = int(N * init_value)
    valid_msg = [1] * K
    valid_index_list, o_msg, _, y_msg, u = BAWGNC_Encode.encode(valid_msg, N, init_value, SNR)
    # 计算SC运行所花费的时间
    start_time = timer()
    for _ in range(cnt):
        u_msg = np.zeros(N, dtype='uint8')  # 保存计算结果
        AWGN_Decode.Polar_Decode(valid_index_list, N, y_msg, u)
    end_time = timer()
    t1 = (end_time - start_time) / cnt
    print("N =", N, "K =", K, " 的情况下\n SC译码所用时间为: ", t1)

    # 计算SCL运行所花费的时间
    start_time = timer()
    for _ in range(cnt):
        AWGN_Decode.AWGN_SCL_Decode(L, valid_index_list, N, y_msg, u)
    end_time = timer()
    t2 = (end_time - start_time) / cnt
    print("N =", N, "K =", K, "L =", L, " 的情况下\n SCL译码所用时间为: ", t2)
    return t1, t2

'''
func:[AWGN信道模型] 对比SC与SCL译码算法的译码准确性
'''

def cmp_AWGN_correct(cnt, N, init_value, SNR, L):
    '''
        c1, c2 分别表示SC, SCL的译码准确率
        计算公式为 (cnt次译码过程中`所有译码正确的比特数量`) / int(N * init_value) * cnt
    '''
    c1 = c2 = 0
    K = int(N * init_value)
    for _ in range(cnt):
        valid_msg = [0, 1] * K
        valid_index_list, o_msg, _, y_msg, u = BAWGNC_Encode.encode(valid_msg, N, init_value, SNR)
        # print("o_msg", o_msg)
        # print("y_msg", y_msg)
        u_res = AWGN_Decode.Polar_Decode(valid_index_list, N, y_msg, u)
        u_scl_res = AWGN_Decode.AWGN_SCL_Decode(L, valid_index_list, N, y_msg, u)
        # u_scl_test = AWGN_Decode.AWGN_SCL_Decode(1, valid_index_list, N, y_msg, u)
        # 检查AWGN信道下 SC和SCL的译码结果是否全部一样
        # is_equal(u_scl_test, u_scl_res)
        # print("u_res", u_res)
        # print("u_scl_res", u_scl_res)
        c1 += cmp_bits(o_msg, u_res, valid_index_list)
        c2 += cmp_bits(o_msg, u_scl_res, valid_index_list)
    c1 = c1 / (K * cnt)
    c2 = c2 / (K * cnt)
    # print("N =", N, "K =", K, " 的情况下\n运行 ", cnt, "次,SC译码准确率为: ", c1)
    # print("N =", N, "K =", K, "L =", L, " 的情况下\n运行 ", cnt, "次,SCL译码准确率为: ", c2)
    return c1, c2

# 传入三个列表 汇出两条曲线图
def draw_picture(x, y1, y2, x_name, y_name, title, label1, label2, y = False):
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.title(title)
    plt.plot(x, y1, label = label1)
    plt.plot(x, y2, label = label2)
    if y:
        plt.ylim((0, 1.1))
    plt.legend()
    plt.show()

# L不变，验证N=N_list的情况下\n所得到的图像
def draw_run_time_N(name, N_list, cnt, init_value, L, SNR):
    # 保存数据
    t1_list, t2_list = [], []
    for N in N_list:
        if name == "BEC":
            t1, t2 = cmp_BEC_run_time(cnt, N, init_value, L)
        else:
            t1, t2 = cmp_AWGN_run_time(cnt, N, init_value, SNR, L)
        t1_list.append(t1)
        t2_list.append(t2)
    x_name = "N"
    y_name = "run time"
    title = name + " && SC && SCL L = " + str(L)
    label1 = "SC"
    label2 = "SCL && L = " + str(L)
    draw_picture(N_list, t1_list, t2_list, x_name, y_name, title, label1, label2)


# N不变，验证L=L_list的情况下\n所得到的图像
def draw_run_time_L(name, N, cnt, init_value, L_list, SNR):
    # 保存数据
    t1_list, t2_list = [], []
    for L in L_list:
        if name == "BEC":
            t1, t2 = cmp_BEC_run_time(cnt, N, init_value, L)
        else:
            t1, t2 = cmp_AWGN_run_time(cnt, N, init_value, SNR, L)
        t1_list.append(t1)
        t2_list.append(t2)
    x_name = "L"
    y_name = "run time"
    title = name + " && SC && SCL && N = " + str(N)
    label1 = "SC"
    label2 = "SCL"
    draw_picture(L_list, t1_list, t2_list, x_name, y_name, title, label1, label2)

# L不变，验证N=N_list的情况下\n所得到的图像
def draw_correct_N(name, N_list, cnt, init_value, L, SNR):
    # 保存数据
    c1_list, c2_list = [], []
    for N in N_list:
        if name == "BEC":
            c1, c2 = cmp_BEC_correct(cnt, N, init_value, L)
        else:
            c1, c2 = cmp_AWGN_correct(cnt, N, init_value, SNR, L)
        c1_list.append(c1)
        c2_list.append(c2)
    x_name = "N"
    y_name = "correct rate"
    title = name + " && SC && SCL L = " + str(L)
    label1 = "SC"
    label2 = "SCL && L = " + str(L)
    draw_picture(N_list, c1_list, c2_list, x_name, y_name, title, label1, label2, True)

# N不变，验证L=L_list的情况下\n所得到的图像
def draw_correct_L(name, N, cnt, init_value, L_list, SNR):
    c1 = 0
    c2_list = [0] * len(L_list)
    K = int(N * init_value)
    for i in range(cnt):
        valid_msg = [1, 0] * K
        if name == "BEC":
            valid_index_list, o_msg, y_msg = Encode.Polar_Encode(valid_msg, N, K, init_value)
            # 假设传输过程中有BEC_Error*N个比特出错
            error_bit_list = Error_Bits.error_bits(N, int(1-BEC_Error*N))
            for err_bit in error_bit_list:
                y_msg[err_bit] = 2  # 设置为2表示传输过程中出错了
            u_msg = np.zeros(N, dtype='uint8')  # 保存计算结果
            u_res = Decode.Polar_Decode(valid_index_list, N, y_msg, u_msg)
        else:
            valid_index_list, o_msg, _, y_msg, u = BAWGNC_Encode.encode(valid_msg, N, init_value, SNR)
            u_res = AWGN_Decode.Polar_Decode(valid_index_list,N,y_msg,u)
        c1 += cmp_bits(o_msg, u_res, valid_index_list)
        for j in range(len(L_list)):
            if name == "BEC":
                u_scl_res = Decode.SCL_Decode(L_list[j], valid_index_list, N, y_msg)
            else:
                u_scl_res = AWGN_Decode.AWGN_SCL_Decode(L_list[j],valid_index_list,N,y_msg,u)
            c2_list[j] += cmp_bits(o_msg, u_scl_res, valid_index_list)
        print(c2_list)
    c1 = c1 / (K * cnt)
    for i in range(len(L_list)):
        c2_list[i] = c2_list[i] / (K * cnt)
    print(c1, c2_list)
    x_name = "L"
    y_name = "correct rate"
    title = name + " && SC && SCL && N = " + str(N)
    label1 = "SC"
    label2 = "SCL"
    draw_picture(L_list, [c1] * len(c2_list), c2_list, x_name, y_name, title, label1, label2, True)

if __name__ == "__main__":
    '''
    参数说明:
        N: 码长
        init_value: 信道传输的有效概率
        L: SCL中保留前L个计算结果
        cnt: 验证准确性时所运行的次数
        BEC_Error: BEC擦除信道的出错概率
    '''
    N = 1024
    init_value = 0.5
    L = 4
    cnt = 2
    SNR = 1.3
    BEC_Error = 0.4
    name = "AWGN"
    # cmp_BEC_run_time(cnt, N, init_value, L)
    # cmp_BEC_correct(cnt, N, init_value, L)
    # cmp_AWGN_run_time(cnt, N, init_value, SNR, L)
    # cmp_AWGN_correct(cnt, N, init_value, SNR, L)
    N_list = [2**i for i in range(2, 11)]
    L_list = [2**i for i in range(6)]
    # draw_run_time_N("BEC", N_list,cnt, init_value, L, SNR)
    # draw_run_time_N(name, N_list,cnt, init_value, L, SNR)
    #
    # draw_run_time_L("BEC", N, cnt, init_value, L_list, SNR)
    # draw_run_time_L(name, N, cnt, init_value, L_list, SNR)
    #
    # draw_correct_N("BEC", N_list, cnt, init_value, L, SNR)
    # draw_correct_N(name, N_list, cnt, init_value, L, SNR)
    #
    # 这里需要修改一下那个原始的error_bit/BEC
    draw_correct_L("BEC", N, cnt, init_value, L_list, SNR)
    # draw_correct_L(name, N, cnt, init_value, L_list, SNR)




