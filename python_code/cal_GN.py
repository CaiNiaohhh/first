from cal_Bn import cal_BN
import numpy, math

# 该步骤的复杂度主要取决于BN的计算以及F的计算
# 其中BN的复杂度已经分析完成了，F的计算过程复杂度为数列
# 1^2，2^2，4^2，8^2，...，N^2 的求和，这个是公比为4的等比数列
#　所以总的复杂度为 N^2
def cal_GN(N):
    BN = cal_BN(N)
    # BN = numpy.mat(numpy.identity(N))
    n = int(math.log2(N))
    # f = numpy.mat(numpy.identity(2))
    f = [[1, 0], [1, 1]]
    F = f
    for i in range(n - 1):
        F = numpy.kron(F, f)
    GN = numpy.dot(BN, F)
    return GN
    # return F

if __name__ == "__main__":
    GN = cal_GN(8)
    print(GN)


