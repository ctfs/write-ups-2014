from xgcd import xgcd

class FiniteGroup:
  '''Super class provides an iterator for self's group.'''

  def group(self, excludeSelf=False):
    '''Iterator over self's whole group if not excludeSelf,
    starting from self or right after it if excludeSelf.
    This version assuming subclass defines instance method next.
    '''
    if not excludeSelf:
      yield self
    f, last = self.next(), None
    while f != self:
      yield f
      f, last = f.next(last), f

  def next(self, prev=None):
    '''Cyclicly return another element of the group.
    This version depends on methods int, likeFromInt, totCodes.
    Optional argument prev ignored in this version.'''
    return self.likeFromInt((int(self)+1) % self.totCodes())


class ParamClass:
  '''Mixin class allows conversion to object with same parameters.
  Assumes method sameParam and constructor that can copy parameters.'''

  def like(self, val):
    '''convert val to a the same kind of object as self.'''
    if self.sameParam(val):
      return val  # avoid unnecessary copy - assumes immutable
    return self.__class__(val, self)

  def tryLike(self, val):
    '''convert val to the same kind of object as self, with the same
    required parameters, if possible, or return None'''
    try:
      return self.like(val)
    except:
      return None

def ZMod(m):
  '''Return a function that makes Mod objects for a particular modulus m.
  '''
  def ModM(coef):
    return Mod(coef, m)
  return ModM


class Mod(FiniteGroup, ParamClass): #subclass of classes above
  '''A class for modular arithmetic, mod m.
  If m is prime, the inverse() method and division operation are always
  defined, and the class represents a field.

  >>> Mod26 = ZMod(26)
  >>> x = Mod26(4)
  >>> y = Mod26(11)
  >>> z = Mod26(39)
  >>> print x+y
  15 mod 26
  >>> print z
  13 mod 26
  >>> print -x
  22 mod 26
  >>> print z - x
  9 mod 26
  >>> print x*8
  6 mod 26
  >>> print x*z
  0 mod 26
  >>> print x**6
  14 mod 26
  >>> print x/y
  24 mod 26
  >>> x == y
  False
  >>> x*y == -8
  True
  >>> e = Mod(1, 5)
  >>> for x in range(1, 5):
  ...   print x, int(e/x)
  1 1
  2 3
  3 2
  4 4
  '''

  #class invarient:
  #  self.m is the modulus
  #  self.value is the usual smallest nonnegative representative

  def __init__(self, n=0, m=None):
    '''Construct a Mod object.
    If n is a Mod, just copy its n and m, and any m parameter should match.
    If m is a Mod, take its m value.
    Otherwise both m and n should be integers, m > 1; construct n mod m.
    '''
    if isinstance(m, Mod):
      m = m.m
    if isinstance(n, Mod):
      assert m is None or m == n.m, 'moduli do not match'
      self.value = n.value; self.m = n.m
      return
    else:
      assert isinstance(m, (int, long)), 'Modulus type must be int or Mod'
      assert m > 1, 'Need modulus > 1'
    assert isinstance(n, (int, long)), 'representative value must be int'
    self.m = m; self.value = n % m

  def __str__(self):   # used by str built-in function, which is used by print
    'Return an informal string representation of object'
    return "{0} mod {1}".format(self.value, self.m)

  def __repr__(self):  # used by repr built-in function
    'Return a formal string representation, usable in the Shell'
    return "Mod({0}, {1})".format(self.value, self.m)

  def sameParam(self, other):
    'True if other is a Mod with same modulus'
    return isinstance(other, Mod) and other.m == self.m

  def __add__(self, other): # used by + infix operand
    'Return self + other, if defined'
    other = self.tryLike(other)
    if other is None: return NotImplemented
    return Mod(self.value + other.value, self.m)

  def __sub__(self, other): # used by - infix operand
    'Return self - other, if defined'
    other = self.tryLike(other)
    if other is None: return NotImplemented
    return Mod(self.value - other.value, self.m)

  def __neg__(self):# used by - unary operand
    'Return -self'
    return Mod(-self.value, self.m)

  def __mul__(self, other): # used by * infix operand
    'Return self * other, if defined'
    other = self.tryLike(other)
    if other is None: return NotImplemented
    return Mod(self.value * other.value, self.m)

  def __div__(self,other):
    'Return self/other if other.inverse() is defined.'
    other = self.tryLike(other)
    if other is None: return NotImplemented
    return self * other.inverse()

  def __eq__(self, other): # used by == infix operand
    '''Return self == other, if defined
    Allow conversion of int to same Mod type before test.  Good idea?'''
    other = self.tryLike(other)
    if other is None: return NotImplemented
    return other.value == self.value

  def __ne__(self, other): # used by != infix operand
    'Return self != other, if defined'
    return not self == other

  # operations where only the second operand is a Mod (prefix r)
  def __radd__(self, other):
    'Return other + self, if defined, when other is not a Mod'
    return self + other # commutative, and now Mod first

  def __rsub__(self, other):
    'Return other - self, if defined, when other is not a Mod'
    return -self + other # can make definite Mod first

  def __rmul__(self, other):
    'Return other * self, if defined, when other is not a Mod'
    return self * other # commutative, and now Mod first

  def __rdiv__(self,other):
    'Return other/self if self.inverse() is defined.'
    return self.inverse() * other # can make definite Mod first

  def __pow__(self, n): # used by ** infix operator
    '''compute power using successive squaring for integer n
    Negative n allowed if self has an inverse.'''
    s = self  # s holds the current square
    if n < 0:
       s = s.inverse()
       n = abs(n)
    return Mod(pow(s.value, n, s.m), s.m)
    # algorithm (but not in C):
##    result = Mod(1, self.m)
##    while n > 0:
##       if n % 2 == 1:
##        result = s * result
##       s = s * s  # compute the next square
##       n = n//2  # compute the next quotient
##    return result

  def __int__(self):
    'Return lowest nonnegative integer representative.'
    return self.value

  def totCodes(self):
    '''Return number of elements in the group.
    This is an upper bound for likeFromInt.'''
    return self.m

  def likeFromInt(self, n):
    '''Int code to Mod object'''
    assert 0 <= n < self.m
    return Mod(n, self.m)

  def __nonzero__(self):
    """Returns True if the current value is nonzero.
    (Used for conversion to boolean.)
    """
    return self.value != 0

  def __hash__(self):
    ''' Hash value definition needed for use in dictionaries and sets.'''
    return hash(self.value)

  def modulus(self):
    '''Return the modulus.'''
    return self.m

  def inverse(self):
    '''Return the multiplicative inverse or else raise a ValueError.'''
    (g,x,y) = xgcd(self.value, self.m)
    if g == 1:
      return Mod(x, self.m)
    raise ValueError, 'Value not invertible'


def doctests():
  ''' More complete tests

  >>> Mod26 = ZMod(26)
  >>> x = Mod26(4)
  >>> y = Mod26(11)
  >>> z = Mod26(39)
  >>> x != y
  True
  >>> x != Mod26(4)
  False
  >>> x != 4
  False
  >>> print 5 - x
  1 mod 26
  >>> print y - 15
  22 mod 26
  >>> print 3*x
  12 mod 26
  >>> print 3+x
  7 mod 26
  >>> Mod26(2**100)  # tests long operand
  Mod(16, 26)
  >>> print y.inverse()
  19 mod 26
  >>> 1/x
  Traceback (most recent call last):
  ...
  ValueError: Value not invertible
  >>> 3 ** x
  Traceback (most recent call last):
  ...
  TypeError: unsupported operand type(s) for ** or pow(): 'int' and 'instance'
  >>> Mod26(2.3)
  Traceback (most recent call last):
  ...
  AssertionError: representative value must be int
  >>> print y**-1
  19 mod 26
  >>> print pow(y, -2)
  23 mod 26
  >>> s = set([x, y]) # uses hash
  >>> x in s
  True
  >>> bool(x)  # true if not 0
  True
  >>> bool(0*x)
  False
  >>> Mod(x, 7)
  Traceback (most recent call last):
  ...
  AssertionError: moduli do not match
  >>> Mod(3, 6.0)
  Traceback (most recent call last):
  ...
  AssertionError: Modulus type must be int or Mod
  >>> Mod(6.0, 3)
  Traceback (most recent call last):
  ...
  AssertionError: representative value must be int
  >>> print(Mod(3, x))
  3 mod 26
  >>> y.likeFromInt(int(x)) == x
  True
  >>> z = Mod(0, 3)
  >>> list(z.group())
  [Mod(0, 3), Mod(1, 3), Mod(2, 3)]
  >>> list((z+1).group(True))
  [Mod(2, 3), Mod(0, 3)]
  '''

if __name__ == '__main__':
  import doctest
  doctest.testmod() #verbose=True)
