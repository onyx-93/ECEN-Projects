Simulated Annealing (SA) is a widely used metaheuristic for solving optimization problems such as the Traveling Salesman Problem, but it has notable limitations. One major issue is its sensitivity to parameter tuning, as performance depends heavily on the choice of initial temperature, cooling schedule, and iteration count. Poorly chosen parameters can either trap the algorithm in local minima or result in excessive computation time. SA’s effectiveness is also strongly influenced by the design of the neighborhood structure. Simple move operators may lead to slow convergence and mediocre solutions, while more advanced operators improve results but increase computational cost. Additionally, the stochastic nature of SA creates variability between runs, requiring multiple trials to ensure reliable performance. These challenges become more pronounced as problem size increases. Overall, while SA can find feasible solutions where simple methods fail, its practical success depends on careful tuning, thoughtful neighborhood design, and often hybridization with other techniques.
####
Quick summary of your 20 trials with 2-opt:

Almost all trials (18 out of 20) reached 3.6047 or 3.6173
Only 2 trials were slightly worse: 3.6103 and 3.9179
Best result: 3.6047 (achieved in 14 trials!)
Worst result: 3.9179 (still very good compared to the old swap version)
Typical range: 3.60–3.62 (very tight spread of ~0.3 units)
This level of consistency and quality is excellent for a 20-city TSP with only 10,000 iterations using Simulated Annealing.

The 3.6047 value you keep hitting repeatedly is almost certainly very close to the global optimum (or possibly the optimum itself) for this particular set of 20 cities.
Why 2-opt improved things so dramatically

##
Random swap only changes the position of two cities → very small, often ineffective move → lots of wasted iterations.
2-opt reverses an entire segment → much more powerful rearrangement → finds better tours much faster.
Even with the same number of iterations (10,000) and same temperature schedule, 2-opt explores the solution space far more effectively.

What this means for your assignment

You now have strong, repeatable evidence that the algorithm works well.
The fact that most runs converge to nearly the same value (3.6047) shows good exploration + proper cooling.
You can confidently report:
Best length found: 3.6047
Average over 20 trials: ≈ 3.62
Mention: "Switching from random swap to 2-opt neighborhood significantly improved consistency and solution quality."

