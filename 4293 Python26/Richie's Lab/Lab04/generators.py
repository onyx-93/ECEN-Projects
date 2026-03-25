def bisection_gen(f, a, b, tol=1e-9, max_it=100):
    fa, fb = f(a), f(b)

    for _ in range(max_it):
        c = 0.5 * (a + b)
        fc = f(c)

        yield c

        if abs(fc) < tol or 0.5 * (b - a) < tol:
            break

        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc

def reg_falsi_gen(f, a, b, tol=1e-9, max_it=100):
    fa, fb = f(a), f(b)
    if fa * fb >= 0:
        raise ValueError("reg_falsi_gen: f(a) and f(b) must have opposite signs.")

    for _ in range(max_it):
        c = (a * fb - b * fa) / (fb - fa)
        fc = f(c)

        yield c

        if abs(fc) < tol:
            break

        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc

def newton_gen(f, df, x0, tol=1e-9, max_it=100):
    x = x0
    for _ in range(max_it):
        fx = f(x)
        dfx = df(x)

        if abs(dfx) < 1e-12:
            raise ValueError("newton_gen: derivative too small.")

        x_next = x - fx / dfx
        yield x_next

        if abs(x_next - x) < tol:
            break

        x = x_next

def secant_gen(f, a, b, tol=1e-9, max_it=100):
    x1, x2 = a, b
    for _ in range(max_it):
        fx1, fx2 = f(x1), f(x2)

        if abs(fx2 - fx1) < 1e-14:
            raise ValueError("secant_gen: denominator too small.")

        x3 = x2 - fx2 * (x2 - x1) / (fx2 - fx1)
        yield x3

        if abs(x3 - x2) < tol:
            break

        x1, x2 = x2, x3

