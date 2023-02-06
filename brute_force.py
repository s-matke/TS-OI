import random
import math
import numpy as np
from genetski import costFunction

def generatePermutations(arr):
    if len(arr) == 0:
        return []
    if len(arr) == 1:
        return [arr]
    permutatedList = [] 
    for i in range(len(arr)):
        extr = arr[i]
        rArr = arr[:i] + arr[i + 1 :]
        for p in generatePermutations(rArr):
            permutatedList.append([extr] + p)
    return permutatedList

def bruteForce(price, mDim, mm):
    permutations = generatePermutations(list(range(mDim)))
    for p in permutations:
        p.append(p[0])
    for index, _ in enumerate(mm):
        mm[index] = permutations[index]
        cost = costFunction(mm[index], price, mDim)
        mm[index].append(cost)
    minPrice = np.inf
    for ar in mm:
        if ar[-1] < minPrice:
            minPrice = ar[-1]
    print("Routes :")
    for index, _ in enumerate(mm):
        if minPrice == mm[index][-1]:
            print(mm[index][:-1], "[" + str(mm[index][-1]) + "]")
    return


def main():
    M = np.array(
        [
            [0, 25, 75, 45], 
            [35, 0, 150, 25], 
            [35, 40, 0, 15], 
            [65, 75, 130, 0]]
    )

    mDim = M.shape[0]

    mL = list(np.zeros((math.factorial(mDim), 2)))

    bruteForce(M, mDim, mL)

if __name__ == "__main__":
    main()