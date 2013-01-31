### Below are a lot of bits of my code, along with Vec2--a lightly modified 
### version of the 2DVectorClass (Vec2d) found at pygame (also appears in the
### excellent pymunk library--some of my modifications came directly from 
### looking at that code!). The original code can be found at the following
### URL: http://www.pygame.org/wiki/2DVectorClass

import math, operator

class Vec2(object):
	__slots__ = ['x', 'y', 'xy']
	def __init__(self, xy_or_x, y = None):
		if y is None:
			self.xy = xy_or_x[0], xy_or_x[1]
			self.x = xy_or_x[0]
			self.y = xy_or_x[1]
		else:
			self.xy = xy_or_x, y
			self.x = xy_or_x
			self.y = y
	def __len__(self):
		return 2
	def __getitem__(self, index):
		if index == 0: return self.x
		elif index == 1: return self.y
		else: raise IndexError("Invalid subscript "+str(key)+" to Vec2")
	def __eq__(self, other):
		if hasattr(other, "__getitem__") and len(other) == 2:
			return self[0] == other[0] and self[1] == other[1]
		else:
			return False
	def __ne__(self, other):
		if hasattr(other, "__getitem__") and len(other) == 2:		
			return self[0] != other[0] or self[1] != other[1]
		else:
			return True
	def __nonzero__(self):
		return self.x != 0.0 or self.y != 0.0
	def _o2(self, other, f):
		if isinstance(other, Vec2):
			return Vec2(f(self.x, other.x),f(self.y, other.y))
		elif (hasattr(other, "__getitem__")):
			return Vec2(f(self.x, other[0]),f(self.y, other[1]))
		else:
			return Vec2(f(self.x, other),f(self.y, other))
	def _r_o2(self, other, f):
		if (hasattr(other, "__getitem__")):
			return Vec2(f(other[0], self.x),f(other[1], self.y))
		else:
			return Vec2(f(other, self.x),f(other, self.y))
	def _io(self, other, f):
		if (hasattr(other, "__getitem__")):
			self.x = f(self.x, other[0])
			self.y = f(self.y, other[1])
			self.xy = (self.x, self.y)
		else:
			self.x = f(self.x, other)
			self.y = f(self.y, other)
			self.xy = (self.x, self.y)
		return self
	def __add__(self, other):
		if isinstance(other, Vec2):
			return Vec2(self.x + other.x, self.y + other.y)
		elif hasattr(other, "__getitem__"):
			return Vec2(self.x + other[0], self.y + other[1])
		else:
			return Vec2(self.x + other, self.y + other)
	__radd__ = __add__
 	def __iadd__(self, other):
		if isinstance(other, Vec2):
			self.x += other.x
			self.y += other.y
			self.xy = (self.x, self.y)
		elif hasattr(other, "__getitem__"):
			self.x += other[0]
			self.y += other[1]
			self.xy = (self.x, self.y)
		else:
			self.x += other
			self.y += other
			self.xy = (self.x, self.y)
		return self
 	def __sub__(self, other):
		if isinstance(other, Vec2):
			return Vec2(self.x - other.x, self.y - other.y)
		elif (hasattr(other, "__getitem__")):
			return Vec2(self.x - other[0], self.y - other[1])
		else:
			return Vec2(self.x - other, self.y - other)
	def __rsub__(self, other):
		if isinstance(other, Vec2):
			return Vec2(other.x - self.x, other.y - self.y)
		if (hasattr(other, "__getitem__")):
			return Vec2(other[0] - self.x, other[1] - self.y)
		else:
			return Vec2(other - self.x, other - self.y)
	def __isub__(self, other):
		if isinstance(other, Vec2):
			self.x -= other.x
			self.y -= other.y
			self.xy = (self.x, self.y)
		elif (hasattr(other, "__getitem__")):
			self.x -= other[0]
			self.y -= other[1]
			self.xy = (self.x, self.y)
		else:
			self.x -= other
			self.y -= other
			self.xy = (self.x, self.y)
		return self
	def __mul__(self, other):
		if isinstance(other, Vec2):
			return Vec2(self.x*other.x, self.y*other.y)
		if (hasattr(other, "__getitem__")):
			return Vec2(self.x*other[0], self.y*other[1])
		else:
			return Vec2(self.x*other, self.y*other)
	__rmul__ = __mul__
	def __imul__(self, other):
		if isinstance(other, Vec2):
			self.x *= other.x
			self.y *= other.y
			self.xy = (self.x, self.y)
		elif (hasattr(other, "__getitem__")):
			self.x *= other[0]
			self.y *= other[1]
			self.xy = (self.x, self.y)
		else:
			self.x *= other
			self.y *= other
			self.xy = (self.x, self.y)
		return self
	def __div__(self, other):
		return self._o2(other, operator.div)
	def __rdiv__(self, other):
		return self._r_o2(other, operator.div)
	def __idiv__(self, other):
		return self._io(other, operator.div)
	def __floordiv__(self, other):
		return self._o2(other, operator.floordiv)
	def __rfloordiv__(self, other):
		return self._r_o2(other, operator.floordiv)
	def __ifloordiv__(self, other):
		return self._io(other, operator.floordiv)
	def __truediv__(self, other):
		return self._o2(other, operator.truediv)
	def __rtruediv__(self, other):
		return self._r_o2(other, operator.truediv)
	def __itruediv__(self, other):
		return self._io(other, operator.floordiv)
	def __mod__(self, other):
		return self._o2(other, operator.mod)
	def __rmod__(self, other):
		return self._r_o2(other, operator.mod)
	def __divmod__(self, other):
		return self._o2(other, operator.divmod)
	def __rdivmod__(self, other):
		return self._r_o2(other, operator.divmod)
	def __pow__(self, other):
		return self._o2(other, operator.pow)
	def __rpow__(self, other):
		return self._r_o2(other, operator.pow)
	def __lshift__(self, other):
		return self._o2(other, operator.lshift)
	def __rlshift__(self, other):
		return self._r_o2(other, operator.lshift)
	def __rshift__(self, other):
		return self._o2(other, operator.rshift)
	def __rrshift__(self, other):
		return self._r_o2(other, operator.rshift)
	def __and__(self, other):
		return self._o2(other, operator.and_)
	__rand__ = __and__
	def __or__(self, other):
		return self._o2(other, operator.or_)
	__ror__ = __or__
	def __xor__(self, other):
		return self._o2(other, operator.xor)
	__rxor__ = __xor__
	def __neg__(self):
		return Vec2(operator.neg(self.x), operator.neg(self.y))
	def __pos__(self):
		return Vec2(operator.pos(self.x), operator.pos(self.y))
	def __abs__(self):
		return Vec2(abs(self.x), abs(self.y))
	def __invert__(self):
		return Vec2(-self.x, -self.y)
	def get_length_sqrd(self):
		return self.x**2 + self.y**2
	def get_length(self):
		return math.sqrt(self.x**2 + self.y**2)
	def __setlength(self, value):
		length = self.get_length()
		self.x *= value/length
		self.y *= value/length
	length = property(get_length, __setlength, None, "gets or sets the magnitude of the vector")
	def rotate(self, angle_degrees):
		radians = math.radians(angle_degrees)
		cos = math.cos(radians)
		sin = math.sin(radians)
		x = self.x*cos - self.y*sin
		y = self.x*sin + self.y*cos
		self.x = x
		self.y = y
 		self.xy = (self.x, self.y)
	def rotated(self, angle_degrees):
		radians = math.radians(angle_degrees)
		cos = math.cos(radians)
		sin = math.sin(radians)
		x = self.x*cos - self.y*sin
		y = self.x*sin + self.y*cos
		return Vec2(x, y)
	def get_angle(self):
		if (self.get_length_sqrd() == 0):
			return 0
		return math.degrees(math.atan2(self.y, self.x))
	def __setangle(self, angle_degrees):
		self.x = self.length
		self.y = 0
		self.xy = (self.x, self.y)
		self.rotate(angle_degrees)
	angle = property(get_angle, __setangle, None, "gets or sets the angle of a vector")
	def get_angle_between(self, other):
		cross = self.x*other[1] - self.y*other[0]
		dot = self.x*other[0] + self.y*other[1]
		return math.degrees(math.atan2(cross, dot))
	def normalized(self):
		length = self.length
		if length != 0:
			return self/length
		return Vec2(self)
	def normalize_return_length(self):
		length = self.length
		if length != 0:
			self.x /= length
			self.y /= length
			self.xy = (self.x, self.y)
		return length
	def perpendicular(self):
		return Vec2(-self.y, self.x)
	def perpendicular_normal(self):
		length = self.length
		if length != 0:
			return Vec2(-self.y/length, self.x/length)
		return Vec2(self)
	def dot(self, other):
		return float(self.x*other[0] + self.y*other[1])
	def get_distance(self, other):
		return math.sqrt((self.x - other[0])**2 + (self.y - other[1])**2)
	def get_dist_sqrd(self, other):
		return (self.x - other[0])**2 + (self.y - other[1])**2
	def projection(self, other):
		other_length_sqrd = other[0]*other[0] + other[1]*other[1]
		projected_length_times_other_length = self.dot(other)
		return other*(projected_length_times_other_length/other_length_sqrd)
	def cross(self, other):
		return self.x*other[1] - self.y*other[0]
	def interpolate_to(self, other, range):
		return Vec2(self.x + (other[0] - self.x)*range, self.y + (other[1] - self.y)*range)
	def convert_to_basis(self, x_vector, y_vector):
		return Vec2(self.dot(x_vector)/x_vector.get_length_sqrd(), self.dot(y_vector)/y_vector.get_length_sqrd())
	def __getstate__(self):
		return [self.x, self.y, self.xy]
	def __setstate__(self, dict):
		self.x, self.y, self.xy = dict
