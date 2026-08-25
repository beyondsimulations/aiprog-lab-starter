# analysis script v2 FINAL (do not delete!!)
# TODO ask Ming where the 2024 data went
import csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

f = open("data/raw/measurements.csv")  # relative path from project root
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

plt.figure()
plt.plot(t2)
plt.title("temperatures")
plt.savefig("data/visualizations/temperature_plot.png")
# plt.show()
# print("rows:", len(d))
