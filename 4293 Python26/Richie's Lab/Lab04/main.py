# Ricardo Landeros Aranda | Oklahoma State University
# ECEN 4293 Applied Numerical Methods in Python
# Spring 2026
# This code and the needed files were completed with the use of generative AI to understand concepts,
# how to apply them, and resolve questions.



from error_func import error_analysis
import generators as gn
import numpy as np

f = lambda x: x**2 - 2.0
df = lambda x: 2.0 * x
x_true = np.sqrt(2.0)

f_2 = lambda x: 2*x**3 + 6*x**2 + x - 3
df_2 = lambda x: 6*x**2 + 12*x + 1 
f2_x_true1 = 0.58114
f2_x_true2 = -1
f2_x_true3 = -2.58114

# p_newtn1 = error_analysis(x_true = x_true, 
#                           f = f,
#                           method_gen = lambda: gn.newton_gen(f, df, 1.0, tol=1e-8, max_it= 20),
#                           max_iter = 20,
#                           tol= 1e-12,
#                           plot_error = True,
#                           plot_convergence = True,
#                           )

# p_bisection = error_analysis(x_true=x_true,
#                              f=f,
#                              method_gen= lambda: gn.bisection_gen(f, 0, 2, tol=1e-8, max_it=20),
#                              max_iter=20,
#                              tol=1e-12,
#                              plot_error=True,
#                              plot_convergence=True,
#                              )

# p_reg_falsi = error_analysis(x_true=x_true,
#                              f=f,
#                              method_gen= lambda: gn.reg_falsi_gen(f, 0, 2, tol=1e-8, max_it=20),
#                              max_iter=20,
#                              tol=1e-12,
#                              plot_error=True,
#                              plot_convergence=True,
#                              )

# p_secant = error_analysis(x_true=x_true,
#                              f=f,
#                              method_gen= lambda: gn.secant_gen(f, 0, 2, tol=1e-8, max_it=20),
#                              max_iter=20,
#                              tol=1e-12,
#                              plot_error=True,
#                              plot_convergence=True,
#                              )

# print(f"\nEstimated order (Newton): {p_newtn1} | Expected order ≈ 2\n")
# print(f"\nEstimated order (Bisection): {p_bisection} | Expected order ≈ 1\n")
# print(f"\nEstimated order (Bisection): {p_reg_falsi} | Expected order ≈ 1\n")
# print(f"\nEstimated order (Bisection): {p_secant} | Expected order ≈ 1.618\n")

# Second Function Testing

p_newtn2 = error_analysis(x_true = f2_x_true1, 
                          f = f,
                          method_gen = lambda: gn.newton_gen(f_2, df_2, 1.0, tol=1e-8, max_it= 20),
                          max_iter = 20,
                          tol= 1e-12,
                          plot_error = True,
                          plot_convergence = True,
                          )

p_bisection2 = error_analysis(x_true= f2_x_true1,
                             f=f,
                             method_gen= lambda: gn.bisection_gen(f_2, 0, 2, tol=1e-8, max_it=20),
                             max_iter=20,
                             tol=1e-12,
                             plot_error=True,
                             plot_convergence=True,
                             )

p_reg_falsi2 = error_analysis(x_true=f2_x_true1,
                             f=f,
                             method_gen= lambda: gn.reg_falsi_gen(f_2, 0, 2, tol=1e-8, max_it=20),
                             max_iter=20,
                             tol=1e-12,
                             plot_error=True,
                             plot_convergence=True,
                             )

p_secant2 = error_analysis(x_true=f2_x_true1,
                             f=f,
                             method_gen= lambda: gn.secant_gen(f_2, 0, 2, tol=1e-8, max_it=20),
                             max_iter=20,
                             tol=1e-12,
                             plot_error=True,
                             plot_convergence=True,
                             )

print(f"\nEstimated order (Newton): {p_newtn2} | Expected order ≈ 2\n")
print(f"\nEstimated order (Bisection): {p_bisection2} | Expected order ≈ 1\n")
print(f"\nEstimated order (Regula Falsi): {p_reg_falsi2} | Expected order ≈ 1\n")
print(f"\nEstimated order (Secant): {p_secant2} | Expected order ≈ 1.618\n")

