.. _decorating-for-dummies:

======================
 What is a decorator?
======================

A decorator is
   a function, that takes a function as input, and returns a
   function

What is a decorator again?

A decorator is
   a function, that takes a function as input, and returns a
   function

Is that really what a decorator is?

No, it isn't (see :ref:`decorating-for-smart-people`) but it is almost
always what a decorator is.  So, for now, let's pretend.  Honestly, it
will help.

Here's an example of a simple decorator:

>>> def mydec(original_func):           
...     print 'Am preparing the function'
...     def _decorating_function(*args):
...         print 'I am running the original function'
...         val = original_func(*args)    
...         print 'I am returning the value from the original function'
...         return val
...     print 'Done preparing, returning new function'
...     return _decorating_function

Note that ``mydec`` takes a function as input, and returns a
function as output.

Now, let's say we have some function ``f1``

>>> def f1(arg):
...     return arg * 10
...
>>> f1(2)
20

We can decorate it with our decorator.  You'll see the decoration
happening in the output below.

>>> f2 = mydec(f1)                   
Am preparing the function
Done preparing, returning new function

Now, running the decorated function (``f2``) reveals the print
statements we put in, in the new function, that the decorator returned.

>>> f2(2)                       
I am running the original function
I am returning the value from the original function
20

This is all very ordinary Python.  But, as of Python 2.4, there is a
special syntax for applying a decorator to a function being
defined.  It uses the ``@`` symbol.  We can use our decorator like this:

>>> @mydec
... def f3(arg):
...     return arg * 20
...
Am preparing the function
Done preparing, returning new function

Running it shows our print statements again:

>>> f3(2)
I am running the original function
I am returning the value from the original function
40

The ``@`` is just a syntax addition, and does exactly the following:

>>> def f3(arg):
...     return arg * 20
...
>>> f3 = mydec(f3)
Am preparing the function
Done preparing, returning new function

which gives exactly the same result as we saw above

>>> f3(2)
I am running the original function
I am returning the value from the original function
40

Using decorators with the ``@`` syntax can be more complicated.

The '@' syntax allows you to put in an *expression*  that returns a
decorator.  Obviously, above, the expression ``'mydec'`` returns the
decorating function ``mydec``. But, you can also enter a more 
complicated expression that returns a decorator.  A decorator is::

   a function, that takes a function as input, and returns a
   function

for example:

>>> def dec_maker(scale_by):
...     # This function, returns a decorator
...     # A decorator is: a function, that takes a function as
...     #    input, and returns a function
...     print 'About to make the decorator'
...     def actual_decorator(func):
...         print 'Applying the actual decorator'
...         def _decorated_func(*args):
...             print 'Running decorated func'
...             val = func(*args)
...             print 'Scaling original return value by %s' % scale_by
...             return val * scale_by
...         return _decorated_func
...     return actual_decorator

Without the ``@`` syntax, you could use ``dec_maker`` like this

>>> resulting_decorator = dec_maker(100)
About to make the decorator
>>> f4 = resulting_decorator(f1)
Applying the actual decorator
>>> f4(2)
Running decorated func
Scaling original return value by 100
2000

The @ equivalent is this:

>>> @dec_maker(100)
... def f4(arg):
...     return arg * 10
...
About to make the decorator
Applying the actual decorator

>>> f4(2)
Running decorated func
Scaling original return value by 100
2000
