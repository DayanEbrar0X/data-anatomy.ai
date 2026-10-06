import numpy as np
loss = lambda w: .5 * (w[0]**2 + 10 * w[1]**2)
grad = lambda w: np.array([w[0], 10 * w[1]])
w = np.array([-4.0, 1.6])        # start high
lr, start = 0.17, loss(w)        # step size
for step in range(30):
    w = w - lr * grad(w)         # step downhill
print(f"{start:.1f} -> {loss(w):.4f}")
