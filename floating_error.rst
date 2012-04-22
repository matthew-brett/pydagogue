####################
Floating point error
####################

This page maybe follows from :ref:`floating-point`

I ran into trouble trying to understand floating point error. After reading
`Wikipedia floating point`_, `Wikipedia machine epsilon`_ and `What every
computer scientist should know about floating point`_, I felt the need of some
more explanation, and so here it is.

***********************
Units at the last place
***********************

Taking the notation from `Every computer scientist`_; let's imagine we have a
floating point number that has base 10 and 3 significand digits, say $3.14
\times 10^1$.  Because we only have 3 digits, the next largest number that we
can represent is obviously $3.15 \times 10^1$.  This number differs from $3.14
\times 10^1$ by one unit in the last place (ULP).  Any real number $z$ that is
between $3.14 \times 10^1$ and $3.15 \times 10^1$ can at best be represented
with one of these two numbers.  Let's say $z$ is actually $\pi$; now
$3.1415926...$ is best represented in our numbers as $3.14 \times 10^1$, and the
rounding error is $\pi - 3.14 \times 10^1 = 0.0015926...$  In the worst case, we
could have some real number $3.145 \times 10^1$ that will have rounding error
0.005.  If we always choose the floating point number nearest to our real number
$z$ then the maximum rounding error occurs when $z$ is halfway between two
representable numbers; in that case the rounding error is 0.5 ULP.

We can generalize to floating point numbers of form:

.. math::

    d_1.d_2...d_p \times \beta^e

Where $p$ is the number of significand digits, $\beta$ is the *base* (10 in our
example), and $e$ is the exponent.

The number is *normalized* if $d_1$ is not zero.

1 ULP corresponds to:

.. math::

    0.00...1 \times \beta^e

where there are $p-1$ zeros in the significand. This is also:

.. math::

    1.0 \times \beta^{e-(p-1)}

Note that any normalized floating point number with exponent $e$ has the same
value for 1 ULP.  Let's define:

.. math::

    ulp(e, p) \to \beta^{e-(p-1)}

We can represent any real number $x$ in normalized floating point format by
using an infinite significand:

.. math::

    d_1.d_2... \times \beta^e

Again, *normalized* means that $d_1 \ne 0$.  The ULP value for a real value $x$
in some some finite floating point format is still $ulp(e, p)$ where $p$ is the
number of significand digits as above.

**************
Absolute error
**************

The IEEE standard for floating point specifies that the result of any floating
point operation should be correct to within the rounding error of the resulting
number.  That is, it specifies that the maximum rounding error for an individual
operation (add, multiply, subtract, divide) should be 0.5 ULP.

In practice it's now very hard indeed to find a machine that does not implement
this rule for floating point operations; all current x86, PPC, ARM chips and
associated compilers do.

Imagine we have two finite floating point numbers $q$ and $r$ and we combine
them using one of the operators {+, -, *, /} in a perfect world at infinite
precision:

.. math::

    x = q \circ r

where $\circ$ is one of the operators {+, -, *, /}. Let's call the actual finite
precision number returned from this calculation $fl(x)$.  The IEEE standard
specifies that $fl(x)$ should be the closest number to $x$ that can be
represented in the finite precision format.

Let $e$ be the exponent of $x$ in normalized infinite floating point, and we
remember that $p$ is the number of significand digits in our finite floating
point format. The IEEE rule then becomes:

.. math::

    \left| fl(x) - x \right| \le 0.5 \times ulp(e, p)

    \left| fl(x) - x \right| \le 0.5 \times \beta^{e-(p-1)}

**************
Relative error
**************

The *relative error* is the rounding error divided by the infinite precision real
number $x$:

.. math::

    \left| \frac{fl(x) - x}{x} \right| \le \frac{0.5 \times \beta^{e-(p-1)}}{x}

However, any value for $x$ that has some exponent $e$ has the same value for
$ulp(e, p) = \beta^{e-(p-1)}$.  Let $m$ be the largest digit in base $\beta$;
thus $m = \beta - 1$.  For example $m = 9$ in base 10 ($\beta = 10$). The values
of $x$ between $1.0 \times \beta^e$ and $m.mmm... \times \beta^e$ all have the
same value for 1 ULP = $\beta^{e-(p-1)}$. The *relative* rounding error will be
greater for smaller $x$ with the same exponent.  Let $a = ulp(e, p)$. When $x =
1.0 \times \beta^e + a$, the relative rounding error is $0.5 \times \beta^{e-(1-p)}
/ (\beta^e + a) \approx 0.5 \times \beta^{e-(1-p)} / \beta^e = 0.5 \times
\beta^{p-1}$.  For $x = m.mm... \times \beta^e$, then $x \approx \beta^{e+1}$
and the largest relative error near this $x$ is $\approx 0.5 \times
\beta^{e-(p-1)} / (\beta^{e+1} - a) \approx 0.5 \times \beta^{e-(p-1)} /
\beta^{e+1} = 0.5 \times \beta^{-p}$.  Therefore the *maximum* relative error
for a $x$ with any exponent $e$ is $\approx 0.5 \times \beta^{1-p}$.

***************
Machine epsilon
***************

Now note that $\beta^{1-p}$ is the ULP for 1; that is $1.0 \times
\beta^{e-(p-1)}$ where $e$ is 0.  Some people refer to this value as *machine
epsilon*, others use that term for $0.5 \times \beta^{1-p}$ - see `variant
definitions`_.  MATLAB and Octave return $\beta^{1-p}$ from their ``eps()``
function. numpy_ uses the same convention in its ``np.finfo`` function.  For
example, the standard ``float32`` single precision type in numpy has $\beta = 2;
p=24$:

>>> import numpy as np
>>> np.finfo(np.float32).eps == 2**(1-24)
True

.. _Wikipedia machine epsilon: http://en.wikipedia.org/wiki/Machine_epsilon
.. _Wikipedia floating point: http://en.wikipedia.org/wiki/Floating_point
.. _variant definitions: http://en.wikipedia.org/wiki/Machine_epsilon#Variant_definitions
.. _What every computer scientist should know about floating point:
      http://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html
.. _Every computer scientist: http://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html
.. _numpy: http://numpy.scipy.org
