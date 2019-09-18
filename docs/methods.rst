Method Behavior in Python
=========================
A method is a function bound to an object in python. Normally an object binds a method by defining it in their class heirarchy (shown below). This example is simple and will be used to demonstrate some properties of methods that are desirable.

.. code:: python
  
  class A:
      def method_1(self):
          pass
  instance_a = A()
  instance_b = A()

Properties
----------

It Works
~~~~~~~~
.. code:: python

    instance_a.method_1() #invokes as expected
    A.method_1(instance_a) #invokes as expected
    
Timing
~~~~~~
Has a distinct start and end to the method

Consistency
~~~~~~~~~~~
.. code:: python

  A.method_1 == A.method_1
  A.method_1 is A.method_1
  instance_a.method_1 == instance_a.method_1
  instance_a.method_1 is instance_a.method_1
  instance_b.method_1 != instance_a.method_1
  instance_b.method_1 is not instance_a.method_1

References
~~~~~~~~~~~~~~~~

Maintains internal references and can be held externally

.. code:: python

    # internal references
    A.method_1.some_attribute = 10
    A.method_1.some_attribute == 10
    # external references
    m = instance_a.method_1
    m() # invokes instance_a's method
    

Decoratable
~~~~~~~~~~~

.. code:: python
    
    class A:
        @decorator_1
        def method_1(self)
