test_object_accessed
--------------------

```eval_rst
.. autofunction:: pythonwhat.test_funcs.test_object_accessed.test_object_accessed
```

    def test_object_accessed(name,
                             times=1,
                             not_accessed_msg=None)

With `test_object()`, you can check whether a student correctly created an object. However, in some cases, you might also be interested whether the student actually used this object to for example assign another object. `test_object_accessed()` makes this possible; it is also possible to test object attributes.

The `name` argument should be a string that specifies the name of the object, or the attribute of a certain object, for which you want to check if it was accesses. If the object resides inside a package, such as `pi` in the `math` package, use `"math.pi"`. With `times`, you can specify how often the object or attribute should have been accessed. With `not_accessed_msg` you can override the automatically generated feedback message in case `name` hasn't been accessed often enough according to `times`.

### Example

To show how everything works, suppose you have the following submission of a student:

    ```
    import numpy as np
    import math as m
    arr = np.array([1, 2, 3])
    x = arr.shape
    print(arr.data)
    print(m.e)
    ```

Let's have a look at some SCT function calls that either pass or fail and why.

- `test_object_accessed("arr")` - PASS: The object `arr` is accessed twice (in `arr.shape` and `arr.data`)
- `test_object_accessed("arr", times=3)` - FAIL: The objet `arr` is only accessed twice.
- `test_object_accessed("arr.shape")` - PASS: The `shape` attribute of `arr` is accessed once.
- `test_object_accessed("math.e")` - PASS: The object `e` inside the `math` package is accessed once (the student uses the alias `m`, but that is not a problem. In case of an error, the automatically generated message will take this into account.)
