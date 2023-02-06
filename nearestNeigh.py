import numpy as np
from genetski import costFunction

def NR(s, r, mL, mDim, mask, price):
    mL[s].append(r)
    mask[:, r] = 1
    mV = np.inf
    mVc = -1
    for col in range(mDim):
        if price[r][col] < mV:
            if mask[r, col] == 0:
                mV = price[r][col]
                mVc = col
    if mVc == -1:
        return
    NR(s, mVc, mL, mDim, mask, price)
    return


def nearestNeighbour(price, mDim, mL, mask):
    
    for row in range(mDim):
        mL[row] = [row]
        mask[:, row] = 1

        minVal = np.inf
        minValCol = -1
        for col in range(mDim):
            if price[row][col] < minVal:
                if mask[row, col] == 0:
                    minVal = price[row][col]
                    minValCol = col
        if minValCol == -1:
            return
        NR(row, minValCol, mL, mDim, mask, price)
        mask = np.zeros((mDim, mDim))
    for index, l in enumerate(mL):
        mL[index].append(mL[index][0])
    for index, l in enumerate(mL):
        cost = costFunction(mL[index], price, mDim)
        mL[index].append(cost)
    print("Routes :")
    for index, l in enumerate(mL):
        print(mL[index][0], ": ", mL[index][:-1], "[" + str(mL[index][-1]) + "]")


def main():
    M = np.array(
        [
            [0, 25, 75, 45], 
            [35, 0, 150, 25], 
            [35, 40, 0, 15], 
            [65, 75, 130, 0]]
    )

    mDim = M.shape[0]

    mask = np.zeros((mDim, mDim))

    mL = list(np.zeros((mDim, 2)))

    nearestNeighbour(M, mDim, mL, mask)

if __name__ == "__main__":
    main()
    