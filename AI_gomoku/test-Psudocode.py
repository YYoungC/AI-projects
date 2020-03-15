FUNCTION hill_climbing(parameters):
    current <- parameters
    while True:
        neighbors <- random.uniform(parameters - somevalue, parameters + somevalue)
                             ENDIF
                              ENDFOR
        IF not neighbors:
            break
        ENDIF
        IF evaluate(neighbors) <= expected_value:
            OUTPUT (neighbors)
            current <- neighbors
            break
        ELSEIF evaluate(neighbors) < evalute(current):
            OUTPUT (neighbors)
            current <- neighbors
