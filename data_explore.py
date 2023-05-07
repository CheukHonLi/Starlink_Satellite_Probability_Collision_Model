"""explore and visualize data"""

import math
import data_reading_utils
import numpy as np
import matplotlib.pyplot as plt

"""debris number vs year(1957-2022) in LEO (160 - 2000km)"""
objects = data_reading_utils.read_data("./data/satcat.csv")
counts = data_reading_utils.get_debris_count_sequence(objects, 160, 2000, 1957, 2022)
years = [year for year in range(1957, 2022 + 1)]
plt.title("Debris Number versus Year in LEO")
plt.xlabel("Year")
plt.ylabel("Debris Number")
plt.plot(years, counts)
# plt.show()
plt.savefig("./result graphs/Debris Number versus Year in LEO.png")
plt.close()

""" debris numbers vs year in range 525 - 535km """
counts = data_reading_utils.get_debris_count_sequence(objects, 525, 535, 1957, 2022)
years = [year for year in range(1957, 2022 + 1)]
plt.title("Debris Number versus Year in Orbit 525 - 535 km")
plt.xlabel("Year")
plt.ylabel("Debris Number")
plt.plot(years, counts)
# plt.show()
plt.savefig("./result graphs/Debris Number versus Year Orbit 525 - 535 km")
plt.close()

# debris number prediction (function)
"""debris number prediction in LEO (160 - 2000) in range 2022 - 2040"""
counts = data_reading_utils.get_debris_count_sequence(objects, 160, 2000, 1957, 2022)
years = [year for year in range(1957, 2022 + 1)][3:]
counts = counts[3:]

# log data
ln_numbers = []
for n in counts:
    ln_numbers.append(math.log(n))

# fit curve
z = np.polyfit(range(1, len(ln_numbers) + 1), ln_numbers, 3)
p = np.poly1d(z)

# fitting y
x = list(range(1, len(ln_numbers) + 1))
y = []
for i in x:
    y.append(p(i))

# plot fitting y vs real y
plt.title("Fitting Debris Number prediction in LEO")
for i in range(len(y)):
    y[i] = np.exp(y[i])
plt.plot(years, y, label="fitting curve")
plt.plot(years, counts, label="ground truth")
plt.xlabel("Year")
plt.ylabel("Debris Number")
plt.legend()
plt.savefig("./result graphs/Fitting Debris Number prediction in LEO")
# plt.show()
plt.close()

"""debris number prediction in 525 - 535 in range 2022 - 2040"""
counts = data_reading_utils.get_debris_count_sequence(objects, 525, 535, 1957, 2022)
years = [year for year in range(1957, 2022 + 1)][3:]
counts = counts[3:]

# log data
ln_numbers = []
for n in counts:
    ln_numbers.append(math.log(n))

plt.plot(years, ln_numbers)
plt.title("Ln Debris Number prediction in Orbit 525 - 535km")
plt.xlabel("Year")
plt.ylabel("Ln Debris Number")
plt.savefig("./result graphs/Ln Debris Number prediction in Orbit 525 - 535km")
plt.close()

# fit curve
z = np.polyfit(range(1, len(ln_numbers) + 1), ln_numbers, 3)
p = np.poly1d(z)

# fitting y
x = list(range(1, len(ln_numbers) + 1))
y = []
for i in x:
    y.append(p(i))

# plot fitting ln y vs real ln y
plt.title("Fitting Ln Debris Number prediction in LEO")
plt.plot(years, y, label="fitting curve")
plt.plot(years, ln_numbers, label="ground truth")
plt.xlabel("Year")
plt.ylabel("Ln Debris Number")
plt.legend()
plt.savefig("./result graphs/Fitting Ln Debris Number prediction in Orbit 525 - 535km")
# plt.show()
plt.close()

# plot fitting y vs real y
plt.title("Fitting Debris Number prediction in Orbit 525 - 535km")
for i in range(len(y)):
    y[i] = np.exp(y[i])
plt.plot(x, y, label="fitting curve")
plt.plot(x, counts, label="ground truth")
plt.legend()
plt.savefig("./result graphs/Fitting Debris Number prediction in Orbit 525 - 535km")
# plt.show()
plt.close()


# predicting the future numbers
x = list(range(1, len(ln_numbers) + 1 + 18))
y = []
for i in x:
    y.append(np.exp(p(i)))
x = list(i + 1960 for i in range(1, len(ln_numbers) + 1 + 18))
plt.title("Predicting Debris Number prediction in Orbit 525 - 535km")
plt.plot(x, y, label="predicting curve")
plt.xlabel("Year")
plt.ylabel("Ln Debris Number")
plt.legend()
plt.savefig("./result graphs/Predicting Debris Number prediction in Orbit 525 - 535km")
# plt.show()
plt.close()


def get_prediction():
    return y
print (y)
#print(dict(zip(x, y)))
