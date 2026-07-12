# analysis script v2 FINAL (do not delete!!)
# TODO ask Ming where the 2024 data went
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

REPO = Path(__file__).resolve().parent
f = open(REPO / "data" / "raw" / "measurements.csv")  # path relative to this file
r = csv.reader(f)
next(r)
d = []
for row in r:
    d.append(row)

# temperatures
t = []
for x in d:
    try:
        v = float(x[3])
    except:
        continue
    t.append(v)

s = 0
for v in t:
    s = s + v
avg = s / len(t)
print("average temperature:", avg)

# humidity
h = []
for x in d:
    try:
        h.append(float(x[5]))
    except:
        pass

s2 = 0
for v in h:
    s2 = s2 + v
print("average humidity:", s2 / len(h))

# same loop again for the plot (copy-paste, kept "just in case")
t2 = []
for x in d:
    try:
        t2.append(float(x[3]))
    except:
        pass

out_dir = REPO / "out"
out_dir.mkdir(exist_ok=True)
plt.figure()
plt.plot(t2)
plt.title("temperatures")
plt.savefig(out_dir / "plot.png")  # relative output path
# plt.show()
# print("rows:", len(d))
