km   = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
mins = [8, 9, 15, 15, 20, 20, 26, 27, 31, 35]
w, b = 0.0, 0.0
for step in range(1000):
    for x, y in zip(km, mins):
        err = w * x + b - y
        w -= 0.002 * err * x
        b -= 0.002 * err
print(f"12 km: {w * 12 + b:.1f} min")
