def bisection(f, a, b, tol=1e-9, max_it=100):

    fa, fb = f(a), f(b) # Inititalize function variables
    roots_list = []

    # if fa * fb >= 0: # Sign check feature
    #     raise ValueError("f(a) and f(b) must have different signs.")
    
    for i in range(max_it): # Iteration through the max amount of attempts
        c = 0.5 * (a + b) # Obtain midpoint
        fc = f(c) # Obtain func value at midpoint
    
        if abs(fc) < tol or 0.5 * (b - a) < tol: # Tolerance satisfaction check
            return c, i, roots_list
    
        if fa * fc < 0: # Limit check and assignment
            b, fb = c, fc
        else:
            a, fa = c, fc
        
        roots_list.append(c)

    return 0.5 * (a + b), i, roots_list # If tolerance not reached, return closest value