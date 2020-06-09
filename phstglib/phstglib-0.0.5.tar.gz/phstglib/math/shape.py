import functools

left_bottom = (0, 0)


def dis(p1, p2):
    return (p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1])


def cross(p0, p1, p2):
    return (p1[0] - p0[0]) * (p2[1] - p0[1]) - (p2[0] - p0[0]) * (p1[1] - p0[1])


def cmp_fun(p1, p2):
    global left_bottom
    c = cross(left_bottom, p1, p2)
    if c == 0:
        return dis(left_bottom, p1) - dis(left_bottom, p2)
    return -c


def graham_scan(points):
    """
    输入点集合， 返回凸包的点集
    """
    if len(points) == 0:
        return []
    global left_bottom
    for i in range(len(points)):
        if points[i][1] < points[0][1]:
            points[0], points[i] = points[i], points[0]
        elif points[i][1] == points[0][1]:
            if points[i][0] < points[0][0]:
                points[0], points[i] = points[i], points[0]
    left_bottom = points[0]
    points[1:] = sorted(points[1:], key=functools.cmp_to_key(cmp_fun))

    # print(points)
    res = []
    for point in points:
        while len(res) > 1:
            if cross(res[-2], res[-1], point) > 0:
                break
            res.pop()
        res.append(point)
    return res


# points = [(0, 0), (1, 0), (2, -1), (2, 1), (1, 2)]
# print(graham_scan(points))
