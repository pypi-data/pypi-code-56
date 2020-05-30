"""
This module can create intervals and perform operations.

In order to bound rounding errors when performing floating point arithmetic,
we can use Interval Arithmetic (IA) to keep track of rounding errors.

After a series of operations using basic operators like +, -, * and / we end
of with an interval instead of an approximation of the result.

The interval width represents the uncertainty of the result but we would know
for sure that the correct result will be within this interval.

An interval is presented by two number representing the lower and upper range
of the interval:

.. math ::
    [a, b]

where :math:`a \\leq b`.

"""
import affapy.aa
from affapy.error import affapyError
import mpmath
from mpmath import (mp, fadd, fsub, fmul, fdiv, fneg, fabs, floor, ceil,
                    sqrt, exp, ln, cos, fmod)


class Interval:
    """
    Representation of an interval.
    An instance of the class **Interval** is composed of two fields:

    * **inf**: the infimum
    * **sup**: the supremum

    """

    def __init__(self, inf, sup):
        """
        Create an interval. It is composed of two fields :
        the infimum and the supremum. If :math:`inf > sup`,
        then the init function reorganize the two values.

        Args:
            inf (int or float or string): infimum
            sup (int or float or string): supremum

        Returns:
            Interval: interval

        Examples:
            >>> from affapy.ia import Interval
            >>> x = Interval(1, 2)
            >>> print(x)
            [1.0, 2.0]

        """
        if inf < sup:
            self._inf = mp.mpf(inf, rounding='f')
            self._sup = mp.mpf(sup, rounding='c')
        else:
            self._inf = mp.mpf(sup, rounding='f')
            self._sup = mp.mpf(inf, rounding='c')

    # Getter
    @property
    def inf(self):
        """Return the inf."""
        return self._inf

    @property
    def sup(self):
        """Return the sup."""
        return self._sup

    # Setter
    @inf.setter
    def inf(self, value):
        """Set the inf."""
        self._inf = value

    @sup.setter
    def sup(self, value):
        """Set the sup."""
        self._sup = value

    # Methods
    def width(self):
        """
        **Width**

        Return the width of an interval:

        .. math ::
            width([a, b]) = b - a

        Args:
            self (Interval): arg

        Returns:
            mpf: sup - inf

        Examples:
            >>> Interval(1, 2).width()
            mpf('1.0')

        """
        return fsub(self.sup, self.inf, rounding='c')

    def mid(self):
        """
        **Middle**

        Return the middle of an interval:

        .. math ::
            middle([a, b]) = \\frac{a + b}{2}

        Args:
            self (Interval): arg

        Returns:
            mpf: (inf + sup) / 2

        Examples:
            >>> Interval(1, 2).mid()
            mpf('1.5')

        """
        return (self.inf + self.sup) / 2

    def radius(self):
        """
        **Radius**

        Return the radius of an interval:

        .. math ::
            radius([a, b]) = \\frac{width([a, b])}{2}

        Args:
            self (Interval): arg

        Returns:
            mpf: width / 2

        Examples:
            >>> Interval(1, 2).radius()
            mpf('0.5')

        """
        return self.width() / 2

    # Unary operator
    def __neg__(self):
        """
        **Operator - (unary)**

        Return the additive inverse of an interval:

        .. math ::
            -[a, b] = [-b, -a]

        Args:
            self (Interval): operand

        Returns:
            Interval: -self

        Examples:
            >>> -Interval(1, 2)
            Interval(-2.0, -1.0)

        """
        return Interval(fneg(self.sup, rounding='f'),
                        fneg(self.inf, rounding='c'))

    # Binary operators
    def __add__(self, other):
        """
        **Operator +**

        Add two intervals:

        .. math ::
            [a, b] + [c, d] = [a + c, b + d]

        Or add an interval and an integer or float or mpf:

        .. math ::
            [a, b] + k = [a + k, b + k]

        Args:
            self (Interval): first operand
            other (Interval or int or float or mpf): second operand

        Returns:
            Interval: self + other

        Raises:
            affapyError: other must be Interval, int, float, mpf

        Examples:
            >>> Interval(1, 2) + Interval(3, 4)
            Interval(4.0, 6.0)
            >>> Interval(1, 2) + 2
            Interval(3.0, 4.0)


        """
        if isinstance(other, self.__class__):
            inf = fadd(self.inf, other.inf, rounding='f')
            sup = fadd(self.sup, other.sup, rounding='c')
            return Interval(inf, sup)
        if isinstance(other, (int, float, mpmath.mpf)):
            inf = fadd(self.inf, mp.mpf(other), rounding='f')
            sup = fadd(self.sup, mp.mpf(other), rounding='c')
            return Interval(inf, sup)
        raise affapyError("other must be Interval, int, float, mpf")

    def __radd__(self, other):
        """
        **Reverse operator +**

        Add two intervals or an interval and an integer or float or mpf.
        See the add operator for more details.

        Args:
            self (Interval): second operand
            other (Interval or int or float or mpf): first operand

        Returns:
            Interval: other + self

        Raises:
            affapyError: other must be Interval, int, float, mpf

        Examples:
            >>> 2 + Interval(1, 2)
            Interval(3.0, 4.0)

        """
        return self + other

    def __sub__(self, other):
        """
        **Operator -**

        Subtract two intervals:

        .. math ::
            [a, b] - [c, d] = [a - c, b - d]

        Or subtract an interval and an integer or float or mpf:

        .. math ::
            [a, b] - k = [a - k, b - k]

        Args:
            self (Interval): first operand
            other (Interval or int or float or mpf): second operand

        Returns:
            Interval: self - other

        Raises:
            affapyError: other must be Interval, int, float, mpf

        Examples:
            >>> Interval(1, 2) - Interval(3, 4)
            Interval(-3.0, -1.0)
            >>> Interval(1, 2) - 3
            Interval(-2.0, -1.0)

        """
        if isinstance(other, self.__class__):
            inf = fsub(self.inf, other.sup, rounding='f')
            sup = fsub(self.sup, other.inf, rounding='c')
            return Interval(inf, sup)
        if isinstance(other, (int, float, mpmath.mpf)):
            inf = fsub(self.inf, mp.mpf(other), rounding='f')
            sup = fsub(self.sup, mp.mpf(other), rounding='c')
            return Interval(inf, sup)
        raise affapyError("other must be Interval, int, float, mpf")

    def __rsub__(self, other):
        """
        **Reverse operator -**

        Subtract two intervals or an interval and an integer or float or mpf.
        See the sub operator for more details.

        Args:
            self (Interval): second operand
            other (Interval or int or float or mpf): first operand

        Returns:
            Interval: other - self

        Raises:
            affapyError: other must be Interval, int, float, mpf

        Examples:
            >>> 1 - Interval(2, 3)
            Interval(-2.0, -1.0)

        """
        return -self + other

    def __mul__(self, other):
        """
        **Operator ***

        Multiply two intervals:

        .. math ::
            [a, b] \\times [c, d] =
            [min\\{a \\times c, a \\times d, b \\times c, b \\times d\\},
            max\\{a \\times c, a \\times d, b \\times c, b \\times d\\}]

        Or multiply an interval and an integer or float or mpf:

        .. math ::
            [a, b] \\times k = [a \\times k, b \\times k]

        Args:
            self (Interval): first operand
            other (Interval or int or float or mpf): second operand

        Returns:
            Interval: self * other

        Raises:
            affapyError: other must be Interval, int, float, mpf

        Examples:
            >>> Interval(1, 2) * Interval(3, 4)
            Interval(3.0, 8.0)
            >>> Interval(1, 2) * 3
            Interval(3.0, 6.0)

        """
        if isinstance(other, self.__class__):
            a, b = self.inf, self.sup
            c, d = other.inf, other.sup
            inf = min([fmul(a, c, rounding='f'), fmul(a, d, rounding='f'),
                       fmul(b, c, rounding='f'), fmul(b, d, rounding='f')])
            sup = max([fmul(a, c, rounding='c'), fmul(a, d, rounding='c'),
                       fmul(b, c, rounding='c'), fmul(b, d, rounding='c')])
            return Interval(inf, sup)
        if isinstance(other, (int, float, mpmath.mpf)):
            return Interval(fmul(mp.mpf(other), self.inf, rounding='f'),
                            fmul(mp.mpf(other), self.sup, rounding='c'))
        raise affapyError("other must be Interval, int, float, mpf")

    def __rmul__(self, other):
        """Reverse operator *

        Multiply two intervals or an interval and an integer or float or mpf.
        See the mul operator for more details.

        Args:
            self (Interval): second operand
            other (Interval or int or float or mpf): first operand

        Returns:
            Interval: other * self

        Raises:
            affapyError: other must be Interval, int, float, mpf

        """
        return self * other

    def __truediv__(self, other):
        """
        **Operator /**

        Divide two intervals:

        .. math ::
            [a, b] / [c, d] = [a, b] \\times [1/d, 1/c]

        or an interval and an integer or float or mpf:

        .. math ::
            [a, b] / k = \\frac{1}{k} \\times [a, b]

        It is possible only if other does not contains 0.

        Args:
            self (Interval): first operand
            other (Interval): second operand

        Returns:
            Interval: self / other

        Raises:
            affapyError: division by 0
            affapyError: other must be Interval, int, float, mpf

        Examples:
            >>> Interval(1, 2) / Interval(3, 4)
            Interval(0.25, 0.666666666666667)
            >>> Interval(1, 2) / 2
            Interval(0.5, 1.0)
            >>> Interval(1, 2) / Interval(-1, 1)
            ...
            affapy.affapyError.affapyError: division by 0

        """
        if isinstance(other, self.__class__):
            c, d = other.inf, other.sup
            if 0 not in other:
                return self * Interval(fdiv(1, d, rounding='c'),
                                       fdiv(1, c, rounding='f'))
            raise affapyError("division by 0")
        if isinstance(other, (int, float, mpmath.mpf)):
            if other != 0:
                return (1 / other) * self
            raise affapyError("division by 0")
        raise affapyError("other must be Interval, int, float, mpf")

    def __pow__(self, n):
        """
        **Operator ****

        Return the power of an interval with another interval or an integer.
        With an interval, it uses the identity:

        .. math ::
            x^n = exp(n \\times log(x))

        Args:
            self (Interval): first operand
            n (Interval or int): second operand (exponent)

        Returns:
            Interval: self ** n

        Raises:
            affapyError: type error: n must be Interval or int

        Examples:
            >>> Interval(1, 2) ** Interval(3, 4)
            Interval(1.0, 16.0)
            >>> Interval(1, 2) ** 3
            Interval(1.0, 8.0)

        """
        if isinstance(n, int):
            if n < 0:
                x = 1 / self
                n = -n
            if n == 0:
                return 1
            y = 1
            x = self.copy()
            while n > 1:
                if n % 2 == 0:
                    x = x * x
                    n = n / 2
                else:
                    y = x * y
                    x = x * x
                    n = (n - 1) / 2
            return x * y
        elif isinstance(n, self.__class__):
            return (n * self.log()).exp()
        raise affapyError("type error: n must be Interval or int")

    # Precision
    def __floor__(self):
        """
        **Function floor**

        Return the floor of an interval:

        .. math ::
            floor([a, b]) = [floor(a), floor(b)]

        You need to import floor from the math library.

        Args:
            self (Interval): arg

        Returns:
            Interval: [floor(inf), floor(sup)]

        Examples:
            >>> from math import floor
            >>> floor(Interval(1.4, 2.5))
            Interval(1.0, 2.0)

        """
        return Interval(floor(self.inf, rounding='f'),
                        floor(self.sup, rounding='c'))

    def __ceil__(self):
        """
        **Function ceil**

        Return the ceil of an interval:

        .. math ::
            ceil([a, b]) = [ceil(a), ceil(b)]

        You need to import ceil from the math library.

        Args:
            self (Interval): arg

        Returns:
            Interval: [ceil(inf), ceil(sup)]

        Examples:
            >>> from math import ceil
            >>> ceil(Interval(1.4, 2.5))
            Interval(2.0, 3.0)

        """
        return Interval(ceil(self.inf, rounding='f'),
                        ceil(self.sup, rounding='c'))

    # Functions
    def __abs__(self):
        """
        **Function abs**

        Return the absolute value of an interval.
        Three possibilities:

        1. If :math:`[a, b] < 0`:

        .. math ::
            abs([a, b]) = [-b, -a]

        2. If :math:`[a, b] > 0`:

        .. math ::
            abs([a, b]) = [a, b]

        3. If :math:`0 \\in [a, b]`:

        .. math ::
            abs([a, b]) = [0, max\\{abs(a), abs(b)\\}]

        Args:
            self (Interval): operand

        Returns:
            Interval: abs(self)

        Examples:
            >>> abs(Interval(-2, -1))
            Interval(1.0, 2.0)
            >>> abs(Interval(1, 2))
            Interval(1.0, 2.0)
            >>> abs(Interval(-2, 1))
            Interval(0.0, 2.0)

        """
        if self < 0:
            return Interval(-self.sup, -self.inf)
        if 0 in self:
            return Interval(0, max(fabs(self.inf),
                                   fabs(self.sup)))
        return self.copy()

    def sqrt(self):
        """
        **Function sqrt**

        Return the square root of an interval:

        .. math ::
            \\sqrt{[a, b]} = [\\sqrt{a}, \\sqrt{b}]

        It is possible only if :math:`a \\geq 0`.

        Args:
            self (Interval): operand

        Returns:
            Interval: sqrt(self)

        Raises:
            affapyError: inf must be >= 0

        Examples:
            >>> Interval(1, 2).sqrt()
            Interval(1.0, 1.4142135623731)
            >>> Interval(-1, 2).sqrt()
            ...
            affapy.affapyError.affapyError: inf must be >= 0

        """
        if self.inf >= 0:
            return Interval(sqrt(self.inf, rounding='f'),
                            sqrt(self.sup, rounding='c'))
        raise affapyError("inf must be >= 0")

    def exp(self):
        """
        **Function exp**

        Return the exponential of an interval:

        .. math ::
            exp([a, b]) = [exp(a), exp(b)]

        Args:
            self (Interval): operand

        Returns:
            Interval: exp(self)

        Examples:
            >>> Interval(1, 2).exp()
            Interval(2.71828182845905, 7.38905609893065)

        """
        return Interval(exp(self.inf, rounding='f'),
                        exp(self.sup, rounding='c'))

    def log(self):
        """
        **Function log**

        Return the logarithm of an interval:

        .. math ::
            log([a, b]) = [log(a), log(b)]

        It is possible only if :math:`a > 0`.

        Args:
            self (Interval): operand

        Returns:
            Interval: log(self)

        Raises:
            affapyError: inf must be > 0

        Examples:
            >>> Interval(1, 2).log()
            Interval(0.0, 0.693147180559945)
            >>> Interval(-1, 2).log()
            ...
            affapy.affapyError.affapyError: inf must be > 0

        """
        if self.inf > 0:
            return Interval(ln(self.inf, roundin='d'),
                            ln(self.sup, rounding='c'))
        raise affapyError("inf must be > 0")

    # Trigo
    def minTrigo(self):
        """
        Return the minimal :math:`2\\pi` periodic interval of an interval.

        Args:
            self (Interval): operand

        Returns:
            Interval: minimal :math:`2\\pi` periodic interval
        """
        inf, sup = self.inf, self.sup
        a = fmod(inf, 2*mp.pi)
        if inf < 0:
            a = fneg(a, rounding='f')
        if fsub(sup, inf) >= 2*mp.pi:
            b = fadd(a, 2*mp.pi, rounding='c')
        else:
            b = fmod(sup, 2*mp.pi)
            if b <= a:
                b = fadd(b, 2*mp.pi, rounding='c')
        return Interval(a, b)

    def cos(self):
        """
        **Function cos**

        Return the cosinus of an interval.
        It considers the minimal :math:`2\\pi` periodic interval
        :math:`[a, b]` of the interval :math:`x`.
        Then:

        1. If :math:`a \\leq \\pi`:

        * if :math:`b \\leq \\pi`:

        .. math ::
            cos(x) = [cos(b), cos(a)]

        * if :math:`\\pi < b \\leq 2\\pi`:

        .. math ::
            cos(x) = [-1, max(cos(a), cos(b))]

        * else:

        .. math ::
            cos(x) = [-1, 1]

        2. If :math:`\\pi < a \\leq 2\\pi`:

        * if :math:`b \\leq 2\\pi`:

        .. math ::
            cos(x) = [cos(a), cos(b)]

        * if :math:`2\\pi < b \\leq 3\\pi`:

        .. math ::
            cos(x) = [min(cos(a), cos(b)), 1]

        * else:

        .. math ::
            cos(x) = [-1, 1]

        Args:
            self (Interval): operand

        Returns:
            Interval: cos(self)

        Examples:
            >>> Interval(1, 2).cos()
            Interval(-0.416146836547142, 0.54030230586814)

        """
        interMinTrigo = self.minTrigo()
        inf, sup = interMinTrigo.inf, interMinTrigo.sup
        if inf <= mp.pi:
            if sup <= mp.pi:
                return Interval(cos(sup), cos(inf))
            if mp.pi < sup <= 2*mp.pi:
                return Interval(-1, max(cos(inf),
                                        cos(sup)))
            return Interval(-1, 1)
        if mp.pi < inf <= 2*mp.pi:
            if sup <= 2*mp.pi:
                return Interval(cos(inf), cos(sup))
            if 2*mp.pi < sup <= 3*mp.pi:
                return Interval(min(cos(inf),
                                    cos(sup)), 1)
            return Interval(-1, 1)

    def sin(self):
        """
        **Function sin**

        Return the sinus of an interval.
        It uses the identity:

        .. math ::
            sin(x) = cos\\left(\\frac{\\pi}{2} - x\\right)

        Args:
            self (Interval): operand

        Returns:
            Interval: sin(self)

        """
        return (-self + mp.pi / 2).cos()

    def tan(self):
        """
        **Function tan**

        Return the tangent of an interval.
        It uses the identity:

        .. math ::
            tan(x) = \\frac{sin(x)}{cos(x)}

        Args:
            self (Interval): operand

        Returns:
            Interval: tan(self)

        """
        return self.sin() / self.cos()

    def cotan(self):
        """
        **Function cotan**

        Return the cotangent of an interval.
        It uses the identity:

        .. math ::
            cotan(x) = \\frac{cos(x)}{sin(x)}

        Args:
            self (Interval): operand

        Returns:
            Interval: cotan(self)

        """
        return self.cos() / self.sin()

    def cosh(self):
        """
        **Function cosh**

        Return the hyperbolic cosine of an interval.
        It uses the identity:

        .. math ::
            cosh(x) = \\frac{exp(x) + exp(-x)}{2}

        Args:
            self (Interval): operand

        Returns:
            Interval: cosh(self)

        """
        return (self.exp() + (-self).exp()) * 0.5

    def sinh(self):
        """
        **Function sinh**

        Return the hyperbolic sine of an interval.
        It uses the identity:

        .. math ::
            sinh(x) = \\frac{exp(x) - exp(-x)}{2}

        Args:
            self (Interval): operand

        Returns:
            Interval: sinh(self)

        """
        return (self.exp() - (-self).exp()) * 0.5

    def tanh(self):
        """
        **Function tanh**

        Return the hyperbolic tangeant of an interval.
        It uses the identity:

        .. math ::
            tanh(x) = \\frac{sinh(x)}{cosh(x)}

        Args:
            self (Interval): operand

        Returns:
            Interval: tanh(self)

        """
        return self.sinh() / self.cosh()

    # Comparison operators
    def __eq__(self, other):
        """
        **Operator ==**

        Compare two intervals.

        Args:
            self (Interval): first operand
            other (Interval): second operand

        Returns:
            bool: self == other

        Raises:
            affapyError: other must be Interval

        Examples:
            >>> Interval(1, 2) == Interval(1, 2)
            True
            >>> Interval(1, 2) == Interval(1, 3)
            False

        """
        if isinstance(other, self.__class__):
            return self.inf == other.inf and self.sup == other.sup
        raise affapyError("other must be Interval")

    def __ne__(self, other):
        """
        **Operator !=**

        Negative comparison of two intervals.

        Args:
            self (Interval): first operand
            other (Interval): second operand

        Returns:
            bool: self != other

        Raises:
            affapyError: other must be Interval

        Examples:
            >>> Interval(1, 2) != Interval(1, 2)
            False
            >>> Interval(1, 2) != Interval(1, 3)
            True

        """
        if isinstance(other, self.__class__):
            return self.inf != other.inf or self.sup != other.sup
        raise affapyError("other must be Interval")

    def __ge__(self, other):
        """
        **Operator >=**

        Greater or equal comparison between two intervals or with
        int, float or mpf.

        Args:
            self (Interval): first operand
            other (Interval or int or float or mpf): second operand

        Returns:
            bool: self >= other

        Raises:
            affapyError: other must be Interval, int, float, mpf

        Examples:
            >>> Interval(1, 2) >= Interval(0, 1)
            True
            >>> Interval(1, 2) >= Interval(0, 2)
            False

        """
        if isinstance(other, self.__class__):
            return self.inf >= other.sup
        if isinstance(other, (int, float, mpmath.mpf)):
            return self.inf >= other
        raise affapyError("other must be Interval, int, float, mpf")

    def __gt__(self, other):
        """
        **Operator >**

        Greater comparison between two intervals or with
        int, float or mpf.

        Args:
            self (Interval): first operand
            other (Interval or int or float or mpf): second operand

        Returns:
            bool: self > other

        Raises:
            affapyError: other must be Interval, int, float, mpf

        Examples:
            >>> Interval(1, 2) > Interval(0, 1)
            False

        """
        if isinstance(other, self.__class__):
            return self.inf > other.sup
        if isinstance(other, (int, float, mpmath.mpf)):
            return self.inf > other
        raise affapyError("other must be Interval, int, float, mpf")

    def __le__(self, other):
        """
        **Operator <=**

        Lesser or equal comparison between two intervals or with
        int, float or mpf.

        Args:
            self (Interval): first operand
            other (Interval or int or float or mpf): second operand

        Returns:
            bool: self <= other

        Raises:
            affapyError: other must be Interval, int, float, mpf

        Examples:
            >>> Interval(1, 2) <= Interval(2, 3)
            True
            >>> Interval(1, 2) <= Interval(1, 3)
            False

        """
        if isinstance(other, self.__class__):
            return self.sup <= other.inf
        if isinstance(other, (int, float, mpmath.mpf)):
            return self.sup <= other
        raise affapyError("other must be Interval, int, float, mpf")

    def __lt__(self, other):
        """
        **Operator <**

        Lesser comparison between two Intervals or with
        int, float or mpf.

        Args:
            self (Interval): first operand
            other (Interval or int or float or mpf): second operand

        Returns:
            bool: self < other

        Raises:
            affapyError: other must be Interval, int, float, mpf

        Examples:
            >>> Interval(1, 2) <= Interval(2, 3)
            False

        """
        if isinstance(other, self.__class__):
            return self.sup < other.inf
        if isinstance(other, (int, float, mpmath.mpf)):
            return self.sup < other
        raise affapyError("other must be Interval, int, float, mpf")

    # Inclusion
    def __contains__(self, other):
        """
        **Operator in**

        Return True if other, who is interval, or int, or float or mpf, is
        in self, who is an interval:

        .. math ::
            x \\in [a, b]

        Args:
            self (Interval): second operand
            other (Interval or Affine or int or float or mpf): first operand

        Returns:
            bool: other in self

        Raises:
            affapyError: if other is not Interval, int, float, Affine, mpf

        Examples:
            >>> Interval(1, 2) in Interval(1, 3)
            True
            >>> Interval(1, 4) in Interval(1, 3)
            False

        """
        if isinstance(other, self.__class__):
            return self.inf <= other.inf and self.sup >= other.sup
        if isinstance(other, (int, float, mpmath.mpf)):
            return self.inf <= other <= self.sup
        if isinstance(other, affapy.aa.Affine):
            return (self.inf <= other.interval.inf
                    and self.sup >= other.interval.sup)
        raise affapyError("other must be Interval, int, float, Affine, mpf")

    def straddles_zero(self):
        """
        Return True if the interval straddles 0, False if not.

        Args:
            self (Interval): operand

        Returns:
            bool: self straddles 0

        """
        return self.inf <= 0 and self.sup >= 0

    # Formats
    def __str__(self):
        """
        **String format**

        Make the string format.

        Args:
            self (Interval): arg

        Returns:
            string: the infimum and the supremum

        Examples:
            >>> print(Interval(1, 2)
            [1, 2]

        """
        return "[{}, {}]".format(self.inf, self.sup)

    def __repr__(self):
        """
        **Repr format**

        Make the repr format.

        Args:
            self (Interval): arg

        Returns:
            string: format

        """
        return "Interval({}, {})".format(self.inf, self.sup)

    def copy(self):
        """
        Copy an interval.

        Args:
            self (Interval): arg

        Returns:
            Interval: self copy

        """
        return Interval(self.inf, self.sup)

    def convert(self):
        """
        Convert an interval :math:`[a, b]` to an affine form:

        .. math ::
            \\hat{x} = x_0 + x_k\\epsilon_k

        with:

        .. math ::
            x_0 = \\frac{a + b}{2} ,
            x_k = \\frac{a - b}{2}

        Args:
            self (Interval): operand

        Returns:
            Affine: affine form associated to the interval

        """
        return affapy.aa.Affine(interval=[self.inf, self.sup])
