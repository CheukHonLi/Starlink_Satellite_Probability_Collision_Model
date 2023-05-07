from object import Object


def read_data(file_name):
    """
    read data from the given file name and then convert them into a list of objects
    :param file_name: the file name of the file
    :return: a list of objects
    """
    objects = []
    f = open(file_name)
    f.readline()
    for line in f.readlines():
        msg = line.strip()
        msg = msg.split(',')
        object_type = msg[3]
        launch_year = int(msg[6].split('-')[0])
        decay_year = msg[8]
        if len(decay_year) > 2:
            decay_year = int(msg[8].split('-')[0])
        else:
            decay_year = 9999
        apogee = float(msg[10]) if len(msg[10]) > 0 else 0
        perigee = float(msg[11]) if len(msg[11]) > 0 else 0
        obj = Object(object_type, launch_year, decay_year, apogee, perigee)
        # print(obj)
        objects.append(obj)
    return objects


def get_debris_count(objects: list[Object], low, high, year):
    """
    get debris count in the given height range and year
    the debris consists of two types: debris and rocket body
    :param objects: a list of the objects
    :param low: low bound of height
    :param high: high bound of height
    :param year: the selected year
    :return: the number of count
    """
    count = 0
    for obj in objects:
        if obj.object_type in ["DEB", "R/B"]:
            if obj.is_alive_in_year(year) and obj.is_in_range(low, high):
                count += 1
    return count


def get_debris_count_sequence(objects: list[Object], low, high, year_start, year_end):
    """
    get debris count sequence in the given height range and year range, the debris consists of two types: debris and rocket body
    :param objects: a list of the objects
    :param low: low bound of height
    :param high: high bound of height
    :param year_start: the start year (included)
    :param year_end: the start year (included)
    :return: a list of count, each count is the corresponding count in that year
    """
    results = []
    for year in range(year_start, year_end + 1):
        count = get_debris_count(objects, low, high, year)
        results.append(count)
    return results


def get_density(low, high, count):
    """
    get density in the given height range
    :param low: low bound of height
    :param high: high bound of height
    :param count: the count in the range
    :return: density, unit: number / km ** 3
    """
    EARTH_RADIUS = 6378.13
    PI = 3.14159
    v = 4/3 * PI * (EARTH_RADIUS + high) ** 3 - 4/3 * PI * (EARTH_RADIUS + low) ** 3
    density = count / v
    return density


if __name__ == "__main__":
    objects = read_data("./data/satcat.csv")
    print(get_debris_count(objects, 0, 9999, 1958))
    print(get_debris_count_sequence(objects, 539, 561, 1958, 2022))
