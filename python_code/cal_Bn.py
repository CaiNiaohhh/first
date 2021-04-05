import numpy
# 转置函数
# 作用是译码的时候可以按照顺序
# 转置既可以转置发送比特的顺序
# 又可以在发送信息和GN相乘后再转置
# 由于kronecker运算都是针对二维矩阵与二维矩阵的，故复杂度是常量，
# 递归程度是logN,每一层是有一个N次的循环，故总的复杂度认为是N*log(N)`
def cal_BN(N):
    if N == 2:
        BN = numpy.mat(numpy.identity(2))
    else:
        RN = [[0 for _ in range(N)] for _ in range(N)]
        for i in range(N):
            if i % 2 == 0:
                RN[i][(i + 1) // 2] = 1
            else:
                RN[i][(i + N) // 2] = 1
        BN = RN * numpy.kron(numpy.mat(numpy.identity(2)), cal_BN(N // 2))
    return BN

if __name__ == "__main__":
    print(cal_BN(8))
