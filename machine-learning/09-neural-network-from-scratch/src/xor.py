import numpy as np
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])
rng = np.random.default_rng(3)
W1, b1 = rng.normal(size=(2, 4)), np.zeros(4)
W2, b2 = rng.normal(size=(4, 1)), np.zeros(1)
lr = 0.5

for step in range(2000):
    h = np.tanh(X @ W1 + b1)
    p = 1 / (1 + np.exp(-(h @ W2 + b2)))
    loss = np.sum((p - y) ** 2) / 2
    if step in (0, 1999):
        print(f"step {step:4}: loss {loss:.3f}")
    dz2 = (p - y) * p * (1 - p)
    dz1 = dz2 @ W2.T * (1 - h ** 2)
    W2 -= lr * h.T @ dz2
    b2 -= lr * dz2.sum(0)
    W1 -= lr * X.T @ dz1
    b1 -= lr * dz1.sum(0)

print("predictions:", *p.round().astype(int).flat)
