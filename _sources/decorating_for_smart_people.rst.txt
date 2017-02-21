.. _decorating-for-smart-people:

==============================
 What is a decorator, really?
==============================

(with thanks to Fernando Perez for setting me straight on this stuff - see http://mail.scipy.org/pipermail/ipython-dev/2009-September/005500.html)

You may want to have a look at the Python docs:

* http://docs.python.org/glossary.html#term-decorator 
* http://docs.python.org/reference/compound_stmts.html#function

The anatomy of the decorator thing is this::

   @decorator-expression
   function-definition

``decorator-expression`` is an *expression* that returns a callable
thing. The callable thing has to take single argument. That's all it is.
``function-definition`` is a function definition (it therefore must
begin with ``def``).  If ``decorator-expression`` is ``dec_func`` and
``function-definition`` is ``def func(): pass`` then the syntax above is
exactly the result of::

   def func(): pass
   func = dec_func(func)

Decorator expression
====================

The decorator expression is an expression that returns a callable thing.

For example, it could be a reference to a callable thing:

>>> def afunc(f): pass
>>> @afunc
... def bfunc(): pass

or an *expression that returns a reference* to a callable thing:

>>> def cfunc(value):
...    def anon_func(f):
...        return value
...    return anon_func
>>> @cfunc('a value')
... def bfunc(): pass

The callable thing can be anything that is callable - for example, a class:

>>> class C(object):
...     def __call__(self, value):
...         pass
>>> @C()
... def bfunc(): pass

The callable thing has to take one argument:

>>> def dfunc(): pass
>>> @dfunc
... def bfunc(): pass
Traceback (most recent call last):
  ...
TypeError: dfunc() takes no arguments (1 given)

and, the callable thing has to be callable:

>>> not_a_func = 'a string'
>>> @not_a_func
... def bfunc(): pass
Traceback (most recent call last):
   ...
TypeError: 'str' object is not callable

The decorator expression result
===============================

The decorator expression result is the result of evaluating the
decorator expression.

For example, in this case:

>>> def cfunc(value):
...    def anon_func(f):
...        return value
...    return anon_func
>>> @cfunc('a value')
... def bfunc(): pass

the decorator expression result is equivalent to:

>>> def anon_func(f):
...     return 'a value'
>>> dec_exp_res = anon_func

Note that, the decorator expression result will process the
``function-definition`` like this:

>>> def func(): pass # function definition
>>> func = dec_exp_res(func)

That is what the syntax says.  Usually, as in
:ref:`decorating-for-dummies`, you will want to return a modified
function.  But, given the syntax, you can do anything you want:

>>> def strange_decorator(f):
...     print 'I am strange'
>>> @strange_decorator
... def bfunc(): pass
I am strange

This fits the syntax (the decorator expression resolves to a callable
thing that takes one argument) but, this time, the decorator just prints
something.  This may seem a little bizarre, but - there are uses...


