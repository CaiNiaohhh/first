import Encode, Decode, AWGN_Decode, BAWGNC_Encode, Error_Bits
import numpy, copy, math, json
import numpy as np

def solve_pre(N, init_value):
    # A, B, C，D, E用来存储待发送的信息
    A, B, C, D, E = {}, {}, {}, {}, {}
    K = int(N * init_value)  # 有效的码长
    u_msg = np.zeros(N, dtype='uint8')  # 保存计算结果
    # 待发送的信息(暂时将有效位设置为1)
    valid_msg = [1] * N
    return A, B, C, D, E, K, u_msg, valid_msg

def solve(A, B, C, D, E):
    count = 0
    for i in range(len(A)):
        if A[i] != D[i]:
            E[count] = i
            count += 1
    res = {}
    res['A'] = A
    res['B'] = B
    res['C'] = C
    res['D'] = D
    res['E'] = E
    res = json.dumps(res)
    return res

def alert(valid_index_list, u_message, y_message):
    if valid_index_list == None:
        print("valid_msg的长度不等于K")
        exit(-1)
    print("有效位信息:", valid_index_list)
    print("原始信息:", u_message)
    print("极化编码后信息:", y_message)

def solve_ABC(A, u_message, y_message, B, N, K, C):
    for i in range(len(u_message)):
        A[i] = u_message[i]
    for i in range(len(y_message)):
        B[i] = y_message[i]
    # 假设传输过程中有N-K个比特出错
    error_bit_list = Error_Bits.error_bits(N, K)
    for err_bit in error_bit_list:
        y_message[err_bit] = 2  # 设置为2表示传输过程中出错了
    print("添加噪声之后的编码信息:", y_message)
    for i in range(len(y_message)):
        C[i] = y_message[i]

def AWGN_solve_ABC(y_msg, A, u_message, y_message, B, N, K, C):
    for i in range(len(u_message)):
        A[i] = u_message[i]
    for i in range(len(y_msg)):
        B[i] = y_msg[i]
    for i in range(len(y_message)):
        C[i] = y_message[i]

def BEC_SC(N, init_value):
    A, B, C, D, E, K, u_msg, valid_msg = solve_pre(N, init_value)
    valid_index_list, u_message, y_message = Encode.Polar_Encode(valid_msg, N, K, init_value)
    alert(valid_index_list, u_message, y_message)
    solve_ABC(A, u_message, y_message, B, N, K, C)
    u_res = Decode.Polar_Decode(valid_index_list, N, y_message, u_msg)
    print("SC极化译码后信息:", u_res)
    for i in range(len(u_res)):
        D[i] = int(u_res[i])
    res = solve(A, B, C, D, E)
    return res


def BEC_SCL(N, init_value, L):
    A, B, C, D, E, K, u_msg, valid_msg = solve_pre(N, init_value)
    valid_index_list, u_message, y_message = Encode.Polar_Encode(valid_msg, N, K, init_value)
    alert(valid_index_list, u_message, y_message)
    solve_ABC(A, u_message, y_message, B, N, K, C)
    u_res = Decode.SCL_Decode(L, valid_index_list, N, y_message)
    print("SCL极化译码后信息:", u_res)
    for i in range(len(u_res)):
        D[i] = int(u_res[i])
    res = solve(A, B, C, D, E)
    return res


def AWGN_SC(N, init_value, SNR):
    A, B, C, D, E, K, u_msg, valid_msg = solve_pre(N, init_value)
    # y_msg表示未加噪声的编码信息
    valid_index_list, u_message, y_msg, y_message, u = BAWGNC_Encode.encode(valid_msg, N, init_value, SNR)
    alert(valid_index_list, u_message, y_message)
    AWGN_solve_ABC(y_msg, A, u_message, y_message, B, N, K, C)
    u_res = AWGN_Decode.Polar_Decode(valid_index_list, N, y_message, u)
    print("AWGN-SC极化译码后信息:", u_res)
    for i in range(len(u_res)):
        D[i] = int(u_res[i])
    res = solve(A, B, C, D, E)
    return res


def AWGN_SCL(N, init_value, SNR, L):
    A, B, C, D, E, K, u_msg, valid_msg = solve_pre(N, init_value)
    valid_index_list, u_message, y_msg, y_message, u = BAWGNC_Encode.encode(valid_msg, N, init_value, SNR)
    alert(valid_index_list, u_message, y_message)
    AWGN_solve_ABC(y_msg, A, u_message, y_message, B, N, K, C)
    u_res = AWGN_Decode.AWGN_SCL_Decode(L, valid_index_list, N, y_message, u)
    print("AWGN-SC极化译码后信息:", u_res)
    for i in range(len(u_res)):
        D[i] = int(u_res[i])
    res = solve(A, B, C, D, E)
    return res