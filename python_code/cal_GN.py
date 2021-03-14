from cal_Bn import cal_BN
import numpy, math

def cal_GN(N):
    BN = cal_BN(N)
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


