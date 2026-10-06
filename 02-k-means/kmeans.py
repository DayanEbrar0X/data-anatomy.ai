import numpy as np
from shops import X       # 300 unlabeled shops
C = X[[234, 263, 286]]        # 3 random guesses
for step in range(8):
    d = ((X[:, None] - C)**2).sum(2)
    g = d.argmin(1)           # nearest center
    C = [X[g == j].mean(0) for j in (0, 1, 2)]
print("group sizes:", *np.bincount(g))
