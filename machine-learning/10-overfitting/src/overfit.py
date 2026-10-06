import numpy as np

rng = np.random.default_rng(149)
temp = np.arange(15, 34)          # 19 days, °C
trend = 300 / (1 + np.exp((24 - temp) / 3))
cones = trend + rng.normal(0, 20, temp.size)
train = temp % 2 == 1             # 10 days
val = ~train                      # 9 unseen days

def rmse(p, days):
    err = np.polyval(p, temp[days]) - cones[days]
    return np.sqrt(np.mean(err ** 2))

scores = []
print("deg  train  val")
for deg in range(1, 10, 2):
    p = np.polyfit(temp[train], cones[train], deg)
    tr, va = rmse(p, train), rmse(p, val)
    scores.append((va, deg))
    print(f"{deg:3} {tr:6.0f} {va:4.0f}")

print("best degree:", min(scores)[1])
