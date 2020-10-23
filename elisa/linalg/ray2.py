from .vec2 import Point2, Vec2

class Ray2(object):
	"""The definition of a ray in 2D-space. The ray is the parametric solution to all points laying on a line 
	emanating from some start point u into direction v.
	"""
	def __init__(self, origin:Point2, direction:Vec2, normalize_direction:bool=True):
		_origin = None
		_direction = None

		_origin = Point2(origin)
		_direction = Vec2(direction)

		if not _origin or not _direction:
			raise ValueError("origin needs to be a tuple or Point2, and direction needs to be a tuple or Vec2")

		self._u = _origin
		self._v = _direction.to_unit() if normalize_direction else direction

	def at(self, t:float):
		return self._u * t + self._v

	@property
	def origin(self):
		return self._u

	@property
	def direction(self):
		return self._v

	def __repr__(self):
		return f"Ray2: {self._u} + t * {self._v}"