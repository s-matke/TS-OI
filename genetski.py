import random
import numpy as np

population_size = 12
iterations = 10
mutation = 0.5
max_iter = 100


def generate_inital_chromosomes(chromosome_length, max, min, pop_size):
    return [random.sample(range(min, max+1), chromosome_length) for i in range(pop_size)]

def costFunction(cityRoute, price, mDim):
    cost = 0
    for i, _ in enumerate(cityRoute):
        if i != mDim:
            cost += int(price[int(cityRoute[i]), int(cityRoute[i+1])])
    return cost


def calculateFitness(cost_func, chromosomes, price, chromosome_length):
    for i, j in enumerate(chromosomes):
        chromosomes[i].append(chromosomes[i][0])
        chromosomes[i].append(cost_func(j, price, chromosome_length))
    return chromosomes

from statistics import median

def natural_selection(chromosomes, population_size):
    P = []
    for index, _ in enumerate(chromosomes):
        P.append(chromosomes[index][-1])

    medianPrice = median(P)
    parents = []
    
    i = 0
    
    for index, _ in enumerate(chromosomes):
        if chromosomes[index][-1] < medianPrice:
            parents.append(chromosomes[index])
            i += 1

    if len(parents) < (population_size / 2):
        for index, _ in enumerate(chromosomes):
            if chromosomes[index][-1] == medianPrice:
                parents.append(chromosomes[index])
            if len(parents) == (population_size / 2):
                break
    return parents

def crossover(pairs):
    children = []
    for i in range(len(pairs)):
        if i % 2 != 0:
            continue
        a1 = pairs[i][:-2]
        a2 = pairs[i + 1][:-2]

        cL = len(a1) // 2
        if len(a1) % 2 == 0:
            cL -= 1
        y1 = a1[: cL + 1]
        y2 = a1[cL + 1 :]

        for ind, _ in enumerate(a2):
            if a2[ind] not in y1:
                y1.append(a2[ind])
            if a2[ind] not in y2:
                y2.append(a2[ind])

        children.append(y1)
        children.append(y2)
    return children

def mutate(children, mutation_rate, chromosome_length):
    mutated_chromosomes = children
    for i in range(len(children)):
        if random.random() < mutation_rate:
            y1 = random.randint(0, chromosome_length - 1)
            y2 = random.randint(0, chromosome_length - 1)
            mutated_chromosomes[i][y1], mutated_chromosomes[i][y2] = mutated_chromosomes[i][y2], mutated_chromosomes[i][y1]
    return children


def print_chromo(chromosomes):
    for i in chromosomes:
        print(i)

def genetic(cost_func, price, population_size, mutation_rate, chromosome_length, max_iter):
    chromosomes = generate_inital_chromosomes(chromosome_length=chromosome_length, max=chromosome_length-1, min=0, pop_size=population_size)
    chromosomes = calculateFitness(cost_func, chromosomes, price, chromosome_length)
    parents = natural_selection(chromosomes, population_size)
    for _ in range(max_iter):
        parents = natural_selection(chromosomes, population_size)
        children = crossover(parents)
        children = mutate(children, mutation_rate, chromosome_length)
        children = calculateFitness(costFunction, children, price, chromosome_length)
        chromosomes = parents + children

    price = np.inf
    route = []
    for ind, _ in enumerate(chromosomes):
        if chromosomes[ind][-1] <= price:
            price = chromosomes[ind][-1]
            route = chromosomes[ind][:-1]
    print(route, "[" + str(price) + "]")

def main():
    M = np.array(
        [
            [0, 25, 75, 45], 
            [35, 0, 150, 25], 
            [35, 40, 0, 15], 
            [65, 75, 130, 0]]
    )
    mDim = M.shape[0]

    genetic(costFunction, M, population_size, mutation, mDim, max_iter=iterations)


if __name__ == "__main__":
    main()
