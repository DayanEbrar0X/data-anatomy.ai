km   = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
mins = [8, 9, 15, 15, 20, 20, 26, 27, 31, 35]
w, b = 0.0, 0.0
lr = 0.02
n = len(km)

for epoch in range(1000):
    dw, db = 0.0, 0.0
    for x, y in zip(km, mins):
        err = w * x + b - y
        dw += err * x / n
        db += err / n
    w -= lr * dw
    b -= lr * db

print(f"mins = {w:.2f} * km + {b:.2f}")
print(f"12 km: {w * 12 + b:.1f} min")
