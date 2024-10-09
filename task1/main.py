import os


def simplex_method(C, A, b, eps=0.00001):
    A = A.copy()
    flag = False
    z = list(map(lambda x: -float(x), C))
    eps = float(strs[-1])
    n = len(z)
    m = len(b)
    bz = 0
    basics = [n + i for i in range(m)]
    for i in range(m):
        for j in range(m):
            A[i].append(1 if i == j else 0)
        z.append(0)
    while True:
        mini = min(z)
        if mini >= 0:
            break
        ind1 = z.index(mini)
        ratio = [-1 if A[i][ind1] == 0 else b[i] / A[i][ind1] for i in range(m)]
        if not any(map(lambda x: x > 0, ratio)):
            flag = True
            break
        ind2 = -1
        for i in range(m):
            if ratio[i] > 0 and (ratio[i] < ratio[ind2] or ind2 == -1):
                ind2 = i
        basics[ind2] = ind1
        d = A[ind2][ind1]
        for i in range(n + m):
            A[ind2][i] /= d
        b[ind2] /= d
        for i in range(m):
            if i == ind2:
                continue
            d = A[i][ind1]
            for j in range(n + m):
                A[i][j] -= A[ind2][j] * d
            b[i] -= b[ind2] * d
        d = z[ind1]
        for i in range(n + m):
            z[i] -= A[ind2][i] * d
        bz -= b[ind2] * d
        if abs(b[ind2] * d) < eps:
            break
    if flag:
        return False, [], 0
    else:
        sol = [0 for _ in range(n + m)]
        for ind, value in enumerate(basics):
            sol[value] = b[ind]
        return True, sol[:n], bz


for file in os.listdir("input"):
    with open(f'input/{file}', 'r') as f:
        strs = f.read().strip().split("\n")
        C0 = strs[0].strip().split()
        A0 = [list(map(float, s.strip().split())) for s in strs[1:-2]]
        b0 = list(map(float, strs[-2].strip().split()))
        eps0 = float(strs[-1])
        res = simplex_method(C0, A0, b0, eps0)
    with open(f'output/{file.strip(".txt")}.txt', 'w') as f:
        if not res[0]:
            f.write("The method is not applicable!")
        else:
            f.write(" ".join(map(lambda x: str(round(x, 5)), res[1])))
            f.write("\n")
            f.write(str(round(res[2], 5)))
