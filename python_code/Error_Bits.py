import random

# 从N个比特中随机选出N-K个比特，置为2
# 先随机产生N个数，对他们的下标进行标记，之后对这些数据排序
# 选取前N-K个下标

def error_bits(N, K):
    random_list = [[i, 0] for i in range(N)]
    for i in range(N):
        random_list[i][1] = random.random()
    random_list = sorted(random_list,key=lambda x:(x[1],x[0]))
    res_list = []
    for i in range(N-K):
        res_list.append(random_list[i][0])
    res_list.sort()
    return res_list

if __name__ == "__main__":
    L = error_bits(8, 6)
    print(L)