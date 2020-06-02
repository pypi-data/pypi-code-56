# from src.tools import vector
# from src.tools.vector import Vector
#
#
# class Rectangle:
#     def __init__(self, start, end, offset=vector.zero):
#         x1, x2 = sorted((start.x, end.x))
#         y1, y2 = sorted((start.y, end.y))
#         self.start = Vector(x1 - offset, y1 - offset)
#         self.end = Vector(x2 + offset, y2 + offset)
#
#     @staticmethod
#     def by_size(start, size, offset=vector.zero):
#         return Rectangle(start, start + size, offset)
#
#     def __contains__(self, item):
#         return self.start.x <= item.x < self.end.x \
#             and self.start.y <= item.y < self.end.y
#
#
# zero = Rectangle(vector.zero, vector.zero)
