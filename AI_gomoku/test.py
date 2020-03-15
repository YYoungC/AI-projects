def hill_climbing(parameters):
    current = parameters
    while True:
        neighbors = random.uniform(parameters - somevalue, parameters + somevalue)
        if not neighbors:
            break
        if evaluate(neighbors) <= expected_value:
            print (neighbors)
            current = neighbors
            break
        elif evaluate(neighbors) < evalute(current):
            print (neighbors)
            current = neighbors
