import numpy as np
from bitstring import BitArray
import random
from operator import itemgetter
import math

alpha = 0.5
beta = 0.5

n_decimals = 4

lower_limit = -100
upper_limit = 100

n_population = 100
cromosome_size = 2

iterations = 100
cross_prob = 0.9
mutation_prob = 0.05
k_adversaries = 3

data = []

def function_fitness(x, y):
	return 0.5 - ( (math.sin(math.sqrt(x**2 + y**2)))**2 -0.5 ) \
					/(1.0 + 0.001*(x**2 + y**2))**2

def test_fitness(x, y):
	return x+y

def get_random_cromosome(lower_limit, upper_limit, n_decimals):
	return round(random.uniform(lower_limit, upper_limit), n_decimals)

def generate_population(n_population, cromosome_size):
	""" Receives as inputs the individuals in a population and cromosome size
    	then generates the population that is saved in the global varible data
    """
	population =  []
	for i in range(0, n_population):
		cromosome_1 = get_random_cromosome(lower_limit, upper_limit, n_decimals)
		cromosome_2 = get_random_cromosome(lower_limit, upper_limit, n_decimals)
		population.append([cromosome_1, cromosome_2])
	print("Generating population:")
	print('\n'.join('  '.join(map(str,i)) for i in population))
	for i in population:
		data.append([i])

def BLX_alpha_crossover(mother_index, father_index):
	cromosome_1 = data[mother_index][0][0] + beta * ( data[father_index][0][0] - \
								data[mother_index][0][0])
	cromosome_2 = data[mother_index][0][1] + beta * ( data[father_index][0][1] - \
								data[mother_index][0][1])
	son = [cromosome_1, cromosome_2]
	return [son]

def eval_population():
	""" reads cromosomes from global variable data and saves to data the returns
		of the function fitness_fuction that uses cromosomes as input
    """

	fitness = []
	for i in data:
		i.append([function_fitness( i[0][0], i[0][1] )])
	

def get_parent(k_adversaries):
	""" picks randomly k elements from the population taking the winner the one with
		more fitness value
	"""
	pool = len(data)
	selected = []

	for i in range(k_adversaries):
		tmp = random.randint(0, pool-1)
		selected.append([tmp, data[tmp][1]])

	index, value = max(enumerate([i[1] for i in selected]), key=itemgetter(1))
	parent_index = selected[index][0]
	return parent_index

def tournament_selection(k_adversaries):
	""" check if the mother and parent is the same tries again to finally return
		the selected indexes
	"""
	selected = []

	print("Selecting by tournament:")
	while(True):
		mother_index = get_parent(k_adversaries)
		father_index = get_parent(k_adversaries)
		if( mother_index != father_index):
			selected.append(mother_index)
			selected.append(father_index)
			break
	print("Mother: " + str(mother_index))
	print("Father: " + str(father_index))

	return selected


def selecting_next_population():
	""" reduces the number of the population just surviving the strongest
	"""
	global data
	print("Selecting next population")
	print('\n'.join(' '.join('                  '.join(map(str, j))for j in i)for i in data))
	tmp = []
	for i,x in zip(data,range(len(data))):
		tmp.append([x, i[1]])
	tmp = sorted(tmp, key=itemgetter(1), reverse=True)
	ms = []
	for i in range(n_population):
		ms.append(data[tmp[i][0]])
	data = ms

def genetic_algorithm():
	""" handles the flow between functions and counts iterations
	"""
	global data
	generate_population(n_population, cromosome_size)
	eval_population()

	for i in range(iterations):
		print("\n\nIteration " + str(i) + " :\n\n")
		print("Evaluating individuals:")
		print('\n'.join(' '.join('   '.join(map(str, j))for j in i)for i in data ))
		tmp = []
		while(True):
			if( len(data) + len(tmp) >= n_population*2):
				break
			if( random.uniform(0,100) <= cross_prob*100 ): # Crossove Prob
				selected = tournament_selection(k_adversaries)
				offspring = BLX_alpha_crossover(selected[0], selected[1])
				for son in offspring:
					if( random.uniform(0,100) <= mutation_prob*100 ): # Mutation Prob
						print("Mutation")
						tmp_son = son
						son[random.randint(0,len(son)-1)] = 1
						print(tmp_son)
						print(son)
					tmp.append([son, [function_fitness(son[0], son[1]) ]])

		for i in tmp:
			data.append(i)
		selecting_next_population()
	print("Evaluating individuals:")
	print('\n'.join(' '.join('              '.join(map(str, j))for j in i)for i in data ))



genetic_algorithm()