import random

def f(x): 
    #return -0.1*x**6 + 0.8*x**4 - 1.5*x**2 + 0.5*x
    #return -0.1*x**6 + 0.7*x**4 - 1.3*x**2 + 0.6*x
    #return -0.02*x**8 - 0.1*x**6 + 0.9*x**4 - 1.4*x**2 + 0.3*x
    return 0.16*x**7-0.6*x**5+3.6*x**3-2.8*x-0.3

def hill_climb(start, step_size,max_iters):
    current = start
    current_value = f(current)
    for _ in range (max_iters):
        next_value_left = f(current - step_size)
        next_value_right = f(current + step_size)
        
        if(next_value_left > next_value_right):
            next_state = current - step_size
            next_value = next_value_left
        else:
            next_state = current + step_size
            next_value = next_value_right 
        if next_value <= current_value:
            break
        current, current_value = next_state, next_value
    return current, current_value

def random_restart_hill_climbing(restarts, step_size, max_iters):
    best_solution = None
    best_value = float('-inf')

    for i in range(restarts):
        start = random.uniform(-2.5, 2.5)
        solution, value = hill_climb(start, step_size, max_iters)
        #print(f"for the {i}'th iteration hill climb, x is {solution}, y is {value}")
        if(value > best_value):
            best_solution, best_value = solution, value


    return best_solution, best_value

def main():
    #start = random.uniform(-2.5,2.5)
    #step_size= 0.1
    #max_iters= 50

    x,y = random_restart_hill_climbing(10, 0.1, 50)
    print(f"final solution is x: {x}, y: {y}")

if __name__ == "__main__":
    main()