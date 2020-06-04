import time
import random


def describe(data: list) -> tuple:
    x_list, y_list = [], []
    for i in data:
        x_list.append(i[0])
        y_list.append(i[1])
    
    return min(x_list), max(x_list), min(y_list), max(y_list)


def sub(data: list) -> tuple:
    des = describe(data)
    xSub = des[1] - des[0]
    ySub = des[3] - des[2]

    return xSub, ySub


def fitting(data: list, scale: float = 0.05) -> list:
    xSub, ySub = sub(data)

    xFloat = round(xSub * scale / 2, 0)
    yFloat = round(ySub * scale / 2, 0)

    res = []
    random.seed(time.time() * 1000)
    for i in data:
        xRandom = random.randint(-xFloat, xFloat)
        yRandom = random.randint(-yFloat, yFloat)

        res.append((i[0] + xRandom, i[1] + yRandom))

    return res


if __name__ == "__main__":
    # random.seed(time.time() * 1000)
    # print(random.randint(-5, 1))
    print([(224, -13), (28, -13), (28, 193), (224, 193), (216, 186), (35, 186), (35, -6), (216, -6)])
    print(fitting([(224, -13), (28, -13), (28, 193), (224, 193), (216, 186), (35, 186), (35, -6), (216, -6)]))
