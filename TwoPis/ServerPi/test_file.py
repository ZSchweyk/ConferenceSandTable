from math import *


def get_theta_range(equation, count_accuracy=10):
    theta = 0
    theta_increment = .001
    cartesian_coordinates = []
    count = 0
    while True:
        # print(theta / pi)
        r = eval(equation)
        # print(r)
        x, y = round(r * cos(theta), 3), round(r * sin(theta), 3)
        print((x, y))
        if (x, y) in cartesian_coordinates:
            print((x, y), "already exists")
            count += 1
        else:
            count = 0

        if count == count_accuracy:
            return theta

        cartesian_coordinates.append((x, y))
        theta += theta_increment



print(get_theta_range("10 * sin(5 * theta)", count_accuracy=3))



