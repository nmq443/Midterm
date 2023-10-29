import math
import random
import matplotlib.pyplot as plt

# get cities data
def getCity():
    cities = []
    f = open('TSP51.txt')
    for i in f.readlines():
        node_city_val = i.split()
        cities.append([node_city_val[0], float(node_city_val[1]), float(node_city_val[2])])

    return cities

# calculate distance between 2 cities
def calculateDistance(cities):
    total_sum = 0
    for i in range(len(cities) - 1):
        cityA = cities[i]
        cityB = cities[i + 1]

        d = math.sqrt(math.pow(cityB[1] - cityA[1], 2) + math.pow(cityB[2] - cityA[2], 2))
        total_sum += d

    cityA = cities[0]
    cityB = cities[-1] 
    total_sum += math.sqrt(math.pow(cityB[1] - cityA[1], 2) + math.pow(cityB[2] - cityA[2], 2))        
    return total_sum

# selecting the population
def selectPopulation(cities, size):
    population = []
    for i in range(size):
        c = cities.copy()
        random.shuffle(c)
        distance = calculateDistance(c)
        population.append([distance, c])

    fitest = sorted(population)[0]
    return population, fitest

# GA
def geneticAlgorithm(population, lenCities, TOURNAMENT_SELECTION_SIZE, MUTATION_RATE, CROSSOVER_RATE, GENERATIONS):
    gen_number = 0
    for i in range(GENERATIONS):
        new_population = []

        # select 2 of the best options we have
        new_population.append(sorted(population)[0])
        new_population.append(sorted(population)[1])

        for j in range( int( ( len(population) - 2 ) / 2 ) ):
        #for j in range( int(len(population))):
            # crossover
            random_number = random.random()
            if random_number < CROSSOVER_RATE:
                parent1 = sorted(random.choices(population, k = TOURNAMENT_SELECTION_SIZE))[0]
                parent2 = sorted(random.choices(population, k = TOURNAMENT_SELECTION_SIZE))[0]
                
                point = random.randint(0, lenCities - 1)

                child1 = parent1[1][0:point]

                for k in parent2[1]:
                    if (k in child1) == False:
                        child1.append(k)
                
                child2 = parent2[1][0:point]

                for k in parent1[1]:
                    if (k in child2) == False:
                        child2.append(k)

            # if crossover not happen
            else:
                child1 = random.choices(population)[0][1]
                child2 = random.choices(population)[0][1]

            # mutation
            if random.random() < MUTATION_RATE:
                point1 = random.randint(0, lenCities - 1)
                point2 = random.randint(0, lenCities - 1)

                child1[point1], child1[point2] = child1[point2], child1[point1]
                
                point1 = random.randint(0, lenCities - 1)
                point2 = random.randint(0, lenCities - 1)
                
                child2[point1], child2[point2] = child2[point2], child2[point1]

            new_population.append([calculateDistance(child1), child1])
            new_population.append([calculateDistance(child2), child2])

        population = new_population
        gen_number += 1

        if gen_number % 10 == 0:
            print(gen_number, sorted(population)[0][0])


    answer = sorted(population)[0]

    return answer, gen_number
                
# draw cities and map
def drawMap(cities, answer):
    for city in cities:
        plt.plot(city[1], city[2], "ro")
        plt.annotate(city[0], (city[1], city[2]))
    
    for city in range(len(answer[1])): # answer[0] is distance and answer[1] is path
        try:
            first = answer[1][city]
            second = answer[1][city+1]

            plt.plot([first[1], second[1]], [first[2], second[2]], "gray")
        
        except:
            continue
    
    first = answer[1][0]
    second = answer[1][-1]
    plt.plot([first[1], second[1]], [first[2], second[2]], "gray")
    plt.show()

def main():
    # initial values
    POPULATION_SIZE = 2000
    TOURNAMENT_SELECTION_SIZE = 4
    MUTATION_RATE = .1
    CROSSOVER_RATE = .9
    GENERATIONS = 200

    cities = getCity()
    firstPopulation, firstFitest = selectPopulation(cities, POPULATION_SIZE)
    answer, genNumber = geneticAlgorithm(firstPopulation, len(cities), TOURNAMENT_SELECTION_SIZE, MUTATION_RATE, CROSSOVER_RATE, GENERATIONS)

    print("\n----------------------------------------------------------------")
    print("Generation: " + str(genNumber))
    print("Fittest chromosome distance before training: " + str(firstFitest[0]))
    print("Fittest chromosome distance after training: " + str(answer[0]))
    # print("Target distance: " + str(TARGET))
    print("----------------------------------------------------------------\n")   
    drawMap(cities, answer)

main()



                
















