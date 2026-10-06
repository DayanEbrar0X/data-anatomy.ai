import numpy as np
r = np.random.default_rng(3)
centers = [(-2.6, 1.2), (2.4, 1.6), (0.2, -1.6)]
X = np.round(np.vstack([r.normal(c, 0.55, (100, 2)) for c in centers]), 3)
