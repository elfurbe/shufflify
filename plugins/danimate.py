import abc
#from shufflify import PluginBase
import random
import math
import numpy

#Genetic Algorithm library classes
from deap import base
from deap import creator
from deap import tools
from deap import algorithms

class PluginBase(object):
    __metaclass__ = abc.ABCMeta

    description = "string"

    @abc.abstractmethod
    def shuffle(self,artists):
        """Do yo' shufflin' bidness and return the array of tracks"""
        tracklist = ""
        return tracklist

def evaluate(individual):
    #TODO - add Adam's other criteria here
        
    #count the number of times an artist plays back-to-back
    N = len(individual)
    count = 0
    for i in xrange(N-1):
        index1 = int(individual[i])
        index2 = int(individual[i+1])
        if songList[index1].sameArtist(songList[index2]) == True:
            count += 1    
    return [count]

class shuffler(PluginBase):

    description = "Dan's Genetic Algorithm juju."

    def shuffle(self,artists):
        #TODO - change this to Multi to accomodate multiple weighting factors
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)
        
        #the number of songs to be shuffled is the number of permutations
        #that each individual must represent
        IND_SIZE = len(artists)
        
        toolbox = base.Toolbox()
        toolbox.register("indices", random.sample, range(IND_SIZE), IND_SIZE)
        toolbox.register("individual", tools.initIterate, creator.Individual,
                         toolbox.indices)
        
        #make the song list global so that it can be accessed in the evaluate() function
        #TODO - see if there is a way to either pass the song list in as an argument to evaluate() or put the songList in each individual
        global songList
        songList = artists
        
        #this is how you can access an individual
        #ind1 = toolbox.individual()
        #ind1.fitness.values = evaluate(ind1)
        #print ind1
        #print ind1.fitness.valid
        #print ind1.fitness
        
        #if you have fewer than the total number of permutations, just
        #evaluate all the permutations at once
        popSize = 100
        if IND_SIZE < 7:
            popSize = math.factorial(IND_SIZE)
                
        #create the population
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)
        pop = toolbox.population(n=popSize)
        
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)
        
        #toolbox.register("mate", tools.cxTwoPoint)
        #toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
        toolbox.register("select", tools.selTournament, tournsize=3)
        toolbox.register("evaluate", evaluate)

        
        NGEN  = 2
        CXPB  = 0.2
        MUTPB = 0.1
        for g in range(NGEN):
            #TODO - add statistics gathering
            
            # Select the next generation individuals
            offspring = toolbox.select(pop, len(pop))
            # Clone the selected individuals
            offspring = map(toolbox.clone, offspring)
            
            #TODO - figure out mating algorithm for permutations
            # Apply crossover on the offspring
            #for child1, child2 in zip(offspring[::2], offspring[1::2]):
            #    if random.random() < CXPB:
            #        toolbox.mate(child1, child2)
            #        del child1.fitness.values
            #        del child2.fitness.values
            
            #TODO - figure out mutation algorithm for permutations
            # Apply mutation on the offspring
            #for mutant in offspring:
            #    if random.random() < MUTPB:
            #        toolbox.mutate(mutant)
            #        del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
                
            # The population is entirely replaced by the offspring
            pop[:] = offspring
        
        
        #TODO - make this more efficient
        #get the best sorting
        best = pop[0]
        minFitness = best.fitness
        for i in xrange(popSize):
            if pop[i].fitness > minFitness:
                minFitness = pop[i].fitness
                best = pop[i]
                
        print "best = " + str(best)
        print "  " + str(best.fitness)
        return best
