"""
predict the collide numbers based on Monte Carllo method
visualize prediction results
"""
import queue
import random

import numpy as np

import data_explore
import data_reading_utils

import multiprocessing

import matplotlib.pyplot as plt
# Satellite period : minute
PERIOD = 95.06

# Repeat Times
REPEAT = 100

# Period in each repeat
ROUND = 100000

EARTH_RADIUS = 6378.13
PI = 3.14159


# parameters: height_low, height_high, safety_distance(50m - 500m), error_bar(contains or not)
def predict_collide(h_low, h_high, debris_count, satellite_count, safety_distance):
    """
    predict the collision number based on the parameters
    :param h_low: the low bound of the height
    :param h_high: the high bound of the height
    :param debris_count: the debris number in the height range
    :param satellite_count: the satellite number in the height range
    :param safety_distance: safety distance of the satellite
    :return: the number of the collision
    """
    mid_height = (h_low + h_high) / 2
    # Radius of 'Doughnut'
    r = (h_high - h_low) / 2
    # Satellite and debris density in selected altitude
    p_satellite = data_reading_utils.get_density(h_low, h_high, satellite_count)
    p_debris = data_reading_utils.get_density(h_low, h_high, debris_count)

    # Volume of 'Doughnut'
    v = (EARTH_RADIUS + mid_height) * 2 * PI * (PI * r ** 2)

    # Number of satellites in 'Doughnut'
    satellites = v * p_satellite
    # 整数部分
    satellite_int = int(satellites)
    satellite_dec = satellites - satellite_int

    # Number of debris in 'Doughnut'
    debris = v * p_debris
    # Integer part of debris
    debris_int = int(debris)
    # Decimal part of debris
    debris_dec = debris - debris_int

    # print(satellite_int, debris)
    collide_counts = []
    for _ in range(REPEAT):
        collide_count = 0
        for i in range(ROUND):
            # Randomly generate satellite and debris
            satellites = []
            debris = []

            # Integer part of satellite
            for j in range(satellite_int):
                s1_x = r * (random.random() * 2 - 1)
                s1_y = r * (random.random() * 2 - 1)
                while not (s1_x ** 2 + s1_y ** 2 <= r ** 2):
                    s1_x = r * (random.random() * 2 - 1)
                    s1_y = r * (random.random() * 2 - 1)
                satellites.append((s1_x, s1_y))
            # Decimal part of satellite
            roll = random.random()
            if roll <= satellite_dec:
                s1_x = r * (random.random() * 2 - 1)
                s1_y = r * (random.random() * 2 - 1)
                while not (s1_x ** 2 + s1_y ** 2 <= r ** 2):
                    s1_x = r * (random.random() * 2 - 1)
                    s1_y = r * (random.random() * 2 - 1)
                satellites.append((s1_x, s1_y))

            # Integer part of debris
            for j in range(debris_int):
                s1_x = r * (random.random() * 2 - 1)
                s1_y = r * (random.random() * 2 - 1)
                while not (s1_x ** 2 + s1_y ** 2 <= r ** 2):
                    s1_x = r * (random.random() * 2 - 1)
                    s1_y = r * (random.random() * 2 - 1)
                debris.append((s1_x, s1_y))
            # Decimal part of debris
            roll = random.random()
            if roll <= debris_dec:
                s1_x = r * (random.random() * 2 - 1)
                s1_y = r * (random.random() * 2 - 1)
                while not (s1_x ** 2 + s1_y ** 2 <= r ** 2):
                    s1_x = r * (random.random() * 2 - 1)
                    s1_y = r * (random.random() * 2 - 1)
                debris.append((s1_x, s1_y))

            # Collision count
            for s in satellites:
                # Check if debris and satellite collide
                # Distance between satellites and debris
                for d in debris:
                    s1_x, s1_y = s[0], s[1]
                    debris_x, debris_y = d[0], d[1]
                    debris_s1 = ((debris_x - s1_x) ** 2 + (debris_y - s1_y) ** 2) ** 0.5
                    if debris_s1 <= safety_distance:
                        collide_count += 1
        collide_counts.append(collide_count)

    standard_error = np.std(collide_counts) / np.sqrt(np.size(collide_counts))
    average_count = sum(collide_counts) / len(collide_counts)
    # print(f"[Finished] safety distance = {safety_distance}")
    return average_count, standard_error

"""Accelerate with multi-processing"""
objects = data_reading_utils.read_data("./data/satcat.csv")

if __name__ == "__main__":

    """539-561km using 2022 debris and satellite data"""
    results = []
    pool = multiprocessing.Pool(multiprocessing.cpu_count()-2)

    debris_count = data_reading_utils.get_debris_count(objects, 539, 561, 2022)
    safety_distances = []
    for i in range(50, 501):
        safety_distance = i / 1000
        results.append(pool.apply_async(func=predict_collide, args=(539, 561, debris_count, 2242, safety_distance)))
    pool.close()
    pool.join()
    print("[Finished] 539-561km using 2022 debris and satellite data")

    new_results = []
    for result in results:
        r = tuple(result.get())
        new_results.append(r)

    new_results.sort(key=lambda x: x[0])

    avg_counts = []
    standard_errors = []
    for r in new_results:
        avg_counts.append(r[0])
        standard_errors.append(r[1])

    # write to file
    with open("./result files/539-561km_mean_error.txt", 'w') as f:
        for i in range(len(avg_counts)):
            f.write(str(avg_counts[i]) + " " + str(standard_errors[i]) + "\n")
    f.close()

    with open("./result files/539-561km_mean_error.txt") as f:
        lines = f.readlines()
    f.close()

    """525-535km using 2022-2040 debris and satellite data"""
    debris_count = data_explore.get_prediction()
    debris_count = sum(debris_count)/len(debris_count)

    results = []
    pool = multiprocessing.Pool(multiprocessing.cpu_count())

    safety_distances = []
    for i in range(50, 501):
        safety_distance = i / 1000
        results.append(pool.apply_async(func=predict_collide, args=(525, 535, debris_count, 10080, safety_distance)))
    pool.close()
    pool.join()
    print("[Finished] 525-535 using 2022-2040 debris and satellite data")

    new_results = []
    for result in results:
        r = tuple(result.get())
        new_results.append(r)

    new_results.sort(key=lambda x: x[0])

    avg_counts = []
    standard_errors = []
    for r in new_results:
        avg_counts.append(r[0])
        standard_errors.append(r[1])

    # write to file
    with open("./result files/525-535km_mean_error.txt", 'w') as f:
        for i in range(len(avg_counts)):
            f.write(str(avg_counts[i]) + " " + str(standard_errors[i]) + "\n")
    f.close()

    with open("./result files/525-535km_mean_error.txt") as f:
        lines = f.readlines()
    f.close()

