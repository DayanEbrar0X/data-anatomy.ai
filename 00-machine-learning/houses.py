import numpy as np
r = np.random.default_rng(7)
x = np.round(r.uniform(1, 9, 40), 2)               # size
y = np.round(3 * x + 4 + r.normal(0, 2, 40), 2)    # price
