from __future__ import annotations

import math
from .linalg import is_numeric, angle_to_rad
from .vec import Vec


class Vec2(Vec):
	"""A two-dimensional floating point vector

	Args:
			Vec ([type]): [description]
	"""
	def __init__(self, a, b=None):
		super(Vec2, self).__init__()
		_a = 0.
		_b = 0.
		if isinstance(a, Vec2):
			_a = a.x
			_b = a.y
		elif isinstance(a, tuple):
			_a = a[0]
			_b = a[1]
		elif is_numeric(a) and is_numeric(b):
			_a = a
			_b = b
		elif a and b:
			_a = float(a)
			_b = float(b)
		else:
			raise ValueError("No value provided ... you can initialize from a vector, from a tuple or from two floats")
		self._v = [_a, _b]

	def __repr__(self):
		return "Vec2[{}, {}]".format(self._v[0], self._v[1])

	def is_zero(self):
		return self._v[0] == 0. and self._v[1] == 0.

	def __add__(self, other):
		return Vec2(self._v[0] + other[0], self._v[1] + other[1])

	def __sub__(self, other):
		return Vec2(self._v[0] - other[0], self._v[1] - other[1])

	def __neg__(self):
		return Vec2(-self._v[0], -self._v[1])

	@staticmethod
	def dot(u:Vec2, v:Vec2) -> float:
		return u[0] * v[0] + u[1] * v[1]

	def project_onto(self, v:Vec2):
		return proj2_u_v(self, v)

	@staticmethod
	def mul(u, v):
		"""Performs element-wise multiplication of two Vec2 instances. If one of the operands is a numeric, 
		it will be broadcast onto all of the corresponding vector elements, i.e. uniform stretch. If both
		operands are numeric the multiplication of the underlying numeric type is used.

		Args:
				u (Vec2, float): The first operand
				v (Vec2, float): The second operand

		Raises:
				ValueError: if the operands are not Vec2 or float types, and exception is raised.

		Returns:
				[Vec2, float]: The result of multiplying the two arguments together element-wise
		"""
		if isinstance(u, Vec2) and is_numeric(v):
			return Vec2(u[0] * v, u[1] * v)
		if is_numeric(u) and isinstance(v, Vec2):
			return Vec2.mul(v, u)
		if isinstance(u, Vec2) and isinstance(v, Vec2):
			return Vec2(u[0] * v[0], u[1] * v[1])
		if is_numeric(u) and is_numeric(v):
			return u * v 
		raise ValueError("u and v must be numeric or Vec2 types")

	@staticmethod
	def div(u, v):
		if isinstance(u, Vec2) and is_numeric(v):
				return Vec2(u[0] / v, u[1] / v)
		if is_numeric(u) and isinstance(v, Vec2):
				return Vec2.div(v, u)
		if isinstance(u, Vec2) and isinstance(v, Vec2):
				return Vec2(u[0] / v[0], u[1] / v[1])
		raise ValueError("u and v must be numeric or Vec2 types")

	def __mul__(self, other):
		return Vec2.mul(self, other)

	def __truediv__(self, other):
		return Vec2.div(self, other)
	
	def to_unit(self):
		"""Returns the two-dimensional unit vector of the underlying vec2 instance.

		Returns:
				[Vec2]: the vector transformed to the two-dimensional unit vector.
		"""		
		d = Vec2.magnitude(self)
		d_inv = 1. / d
		return Vec2(self.x * d_inv, self.y * d_inv)

	@property
	def x(self):
		return self._v[0]

	@property
	def y(self):
		return self._v[1]

	@staticmethod
	def magnitude(u):
		_x = u.x
		_y = u.y
		return math.sqrt(_x**2 + _y**2)

	@staticmethod
	def unit_vector(u):
		"""Returns the two-dimensional unit-vector of u.

		Args:
				u ([Vec2]): The two-dimensional vector which to convert to a unit vector

		Returns:
				[Vec2]: The unit vector of
		"""
		l = Vec2.magnitude(u)
		linv = 1./l
		return u * linv	

	def to_tuple(self) -> tuple:
		"""Turns the vector into a tuple representation

		Returns:
				tuple: the vector representated as a tuple
		"""
		return self._v[0], self._v[1]

	@staticmethod
	def from_angle(angle_rad:float, to_unit:bool=True):
		y = math.sin(angle_rad)
		x = math.cos(angle_rad)
		v = Vec2(a=x, b=y)
		if to_unit:
			v = v.to_unit()
		return v

	def to_angle(self) -> float:
		"""Returns the angle in radians formed by the vector and the 2D x-axis

		Returns:
				[float]: The angle in radians
		"""
		return math.atan2(self.y, self.x)

Point2 = Vec2
zero0 = Vec2(0, 0)
one2 = Vec2(1, 1)

def proj2_u_v(u: Vec2, v: Vec2) -> Vec2:
	"""
	Returns the projection of vector u onto vector v
	:param u: (Vec) vector u
	:param v: (Vec) vector v
	:return: (Vec) the projection
	"""
	if v.is_zero():
		raise ValueError("v cannot be the zero vector")
	uv = Vec2.dot(u, v)
	k  = uv * v.length_squared_inv()
	return v * k