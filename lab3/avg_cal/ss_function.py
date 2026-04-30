import random

def quickpower(a, b, p):
    a = a % p
    ans = 1
    while b != 0:
        if b & 1: ans = (ans * a) % p
        b >>= 1
        a = (a * a) % p
    return ans

def get_polynomial(x0, T, p, fname):
    f = [x0]
    for i in range(T):
        f.append(random.randrange(0, p))
    return f

def count_polynomial(f, x, p):
    ans = f[0]
    for i in range(1, len(f)):
        ans = (ans + f[i] * quickpower(x, i, p)) % p
    return ans

def restructure_polynomial(x, fx, t, p):
    ans = 0
    for i in range(t):
        fx[i] = fx[i] % p
        fxi = 1
        for j in range(t):
            if j != i:
                # 模块化逆元计算
                fxi = (-1 * fxi * x[j] * quickpower(x[i] - x[j], p - 2, p)) % p
        fxi = (fxi * fx[i]) % p
        ans = (ans + fxi) % p
    return ans % p
