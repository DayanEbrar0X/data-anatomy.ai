import numpy as np
from houses import x, y           # 40 examples
w, b = 0.0, 0.0                   # the model
for epoch in range(2000):
    err = w * x + b - y           # how wrong
    w -= 0.01 * (err * x).mean()  # nudge w
    b -= 0.01 * err.mean()        # nudge b
print(f"price = {w:.2f} * size + {b:.2f}")
