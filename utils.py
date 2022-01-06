import math


class Vector:
	def __init__(self, x, y, length=None):
		self.x = x
		self.y = y
		if length is not None:
			self.set_length(length)

	def get_length(self):
		return math.hypot(self.x, self.y)

	def set_length(self, length):
		my_length = self.get_length()
		if my_length != 0:
			k = length / my_length
			self.x *= k
			self.y *= k

	def rounded(self):
		return Vector(round(self.x), round(self.y))

	def length(self, length):
		return Vector(self.x, self.y, length)

	def __mul__(self, other: int):
		return Vector(other * self.x, other * self.y)

	def __str__(self):
		return f"({self.x},{self.y})"


class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y

	def get(self):
		return self.x, self.y

	def __add__(self, other):
		return Point(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return Vector(self.x - other.x, self.y - other.y)

	def __str__(self):
		return f"({self.x},{self.y})"


def min_abs(*args):
	result = args[0]
	for e in args:
		if abs(e) < abs(result):
			result = e
	return result
