import random


def main():
    while True:
        target_str = input("Enter a sequence of space-seperated integers (ex: 1 2 -3) | [Q]uit: ")
        if target_str == "Q":
            return
        try:
            target = [int(val) for val in target_str.split(" ")]
            print("You can produce", target_str, "with command:",  create_program(target, interpret), "\n")
        except:
            print("Invalid Argument.\n")
    
    
def interpret(program, array):
    loc = 0
    for command in program:
        if command == "+":
            array[loc] += 1
        elif command == "-":
            array[loc] -= 1
        elif command == ">":
            try:
                val = array[loc + 1]
                loc += 1
            except:
                raise RuntimeError
        elif command == "<":
            if loc <= 0:
                raise RuntimeError
            else:
                loc -= 1


def evaluate_fitness(program, target, interpreter):
    try:
        memory = [0 for bucket in range(len(target))]
        interpreter(program, memory)
        try:
            val = target.compare(memory) 
        except:
            val = compare(target, memory)
        return val
    except:
        return float("inf")

 
def make_pop(lower_bound):
    population_size = 500
    population = []
    while len(population) < population_size:
        program = "".join([random.choice("<>+-") for i in range(lower_bound)])
        population.append(program)   
    return population


def abs_sum(target):
    sum = 0
    for val in target:
        sum += abs(val)
    return sum
   

def compare(target, interpreted):
    sum = 0
    for i in range(len(target)):
        sum += abs(target[i] - interpreted[i])
    return sum    


def crossover(program_x, program_y):
    min_len = min(len(program_x), len(program_y))
    split = random.randint(1, min_len)
    child1 = program_x[:split] + program_y[split:]
    child2 = program_y[:split] + program_x[split:]
    return (child1, child2)


def crossover_with_mutation(program_x, program_y):
    magical_probability = len(program_x) / 2
    max_probability = 100
    child1, child2 = crossover(program_x, program_y)
    prob_mutation = random.randint(0, max_probability)
    if prob_mutation < magical_probability: 
        mut = random.choice("+<>-")
        min_len = min(len(program_x), len(program_y))
        loc = random.randint(0, min_len)
        if prob_mutation < magical_probability: 
            child1 = child1[:loc] + mut + child1[loc:]
            child2 = child2[:loc] + mut + child2[loc:]
        else:
            child1 = child1[:loc] + mut + child1[loc + 1:]
            child2 = child2[:loc] + mut + child2[loc + 1:]
    return (child1, child2)


def make_next_gen(top_best):
    population_size = 500
    next_gen = []
    i = 0
    while len(next_gen) < population_size:
        program1 = top_best[i]
        program2 = top_best[random.randint(0, len(top_best) - 1)]
        child1, child2 = crossover_with_mutation(program1, program2)
        next_gen.append(child1)
        next_gen.append(child2)
        i = (i + 1) % len(top_best)
    return next_gen


def create_program(target, interpreter):
    magical_coefficient = (2 * len(target)) - 1
    top_best_size = 50
    try:
        if abs_sum(target) == 0:
            return ""
        curr_gen = make_pop(abs_sum(target) + magical_coefficient)
    except:
        if target.abs_sum() == 0:
            return ""
        curr_gen = make_pop(target.abs_sum() + magical_coefficient)
    while True:
        gen_costs = ([evaluate_fitness(program, target, interpreter) 
                    for program in curr_gen])
        if 0 in gen_costs:
            poss_sol = curr_gen[gen_costs.index(0)]
            memory = [0 for i in range(len(target))]
            interpreter(poss_sol, memory)
            try:
                if target.compare(memory) == 0:
                    return poss_sol
            except:
                if compare(target, memory) == 0:
                    return poss_sol
        total_score = sum([cost for cost in gen_costs if cost != float("inf")])
        top_best = []
        for i in range(top_best_size):
            best_score = min(gen_costs)
            best_id = gen_costs.index(best_score)
            gen_costs.remove(best_score)
            top_best.append(curr_gen[best_id])
            curr_gen.pop(best_id)
        curr_gen = make_next_gen(top_best)


if __name__ == "__main__":
    main()
