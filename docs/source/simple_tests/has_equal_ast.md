has_equal_ast
--------------

```eval_rst
.. autofunction:: pythonwhat.check_funcs.has_equal_ast
```

An abstract syntax tree (AST) is a way of representing the high-level structure of python code.

### Example: quotes

Whether you use the concrete syntax `x = "1"` or `x = '1'`, the abstract syntax is the same: x is being assigned to the string "1".

### Example: parenthesis

Grouping by parentheses produces the same AST, when the same statement would work the same without them.
For example, `(True or False) and True`, and `True or False and True`, are the same due to operator precedence.

### Example: spacing

The same holds for different types of spacing that essentially specify the same statement: `x     = 1` or `x = 1`.

### Caveat: evaluating

What the AST doesn't represent is values that are found through evaluation. For example, the first item in the list in

```python
x = 1
[x, 2, 3]
```

and

```python
[1, 2, 3]
```

Is not the same. In the first case, the AST represents that a variable `x` needs to be evaluated in order to find out what its value is. In the second case, it just represents the value `1`.
