from roboticstoolbox import *
from spatialmath.base import *
import math

TZ0 = numpy.array([[1, 0, 0, 0],[0, 1, 0, 0],[0, 0, 1, a1],[0, 0, 0, 1]])
RZ0 = numpy.array([[cos(q1), -sin(q1), 0, 0],[sin(q1), cos(q1), 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]])
TX1 = numpy.array([[1, 0, 0, a2],[0, 1, 0, 0],[0, 0, 1, 0],[0, 0, 0, 1]])
RX1 = numpy.array([[1, 0, 0, 0],[0, cos(pi/2), -sin(pi/2), 0],[0, sin(pi/2), cos(pi/2), 0],[0, 0, 0, 1]])
T01 = multi_dot([TZ0,RZ0,TX1,RX1])
print(f'T01 = {T01}')
T01 = multi_dot([RZ0,TZ0,RX1,TX1])
print(f'T01 = {T01}')