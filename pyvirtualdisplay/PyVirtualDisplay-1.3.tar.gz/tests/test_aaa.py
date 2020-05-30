# import os

# from pyvirtualdisplay import Display
# from pyvirtualdisplay.xephyr import XephyrDisplay


# def test_strange_osx_bug():
#     with Display() as d1:
#         print(d1.is_alive())
#         with XephyrDisplay() as d:
#             pass
#         print(d1.is_alive())

#         with Display() as d:
#             pass
#         print(d1.is_alive())

#         # Xephyr cannot open host display. Is DISPLAY set?
#         with XephyrDisplay() as d:
#             pass
