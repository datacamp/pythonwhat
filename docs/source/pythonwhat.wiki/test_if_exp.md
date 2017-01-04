test_if_exp
-----------

```eval_rst
.. autofunction:: pythonwhat.test_funcs.test_if_else.test_if_exp
```

`test_if_exp` is a wrapper around `test_if_else`, which tells it to look for inline `if` expressions. As such, it uses the same arguments. [See `test_if_else` for more info](test_if_else.md).

### What is an inline `if` expression?

An inline `if` expression looks like..

```{python}
x = 'a' if True else 'b'
```

This is in contrast to an `if` block, which looks like..

```{python}
if True:
    x = 'a'
else:
    x = 'b'
```

### Parts

This test tries to break code into 3 parts, BODY, TEST, and ORELSE.
The table below shows an example inline `if` expression on the left,
and the parts that would be extracted on the right.

| code                      | parts breakdown |
| ------------------------- | --------------------- |
| `x = 'a' if True else 'b'` | `x = BODY if TEST else ORELSE` |

### Nested `if` expressions

Just like `test_if_else`, `test_if_exp` will not find a nested `if` expression. 
Instead, the nested portion will be inside one of the parts.
For example, below is an exercise with an `if` expression in the ORELSE part of another `if` expression.

*** =solution
```{python}
x = 'a' if True else ('b' if False else 'c')
```

*** =sct
```{python}
test_if_exp(orelse=lambda: test_if_exp(orelse=lambda: test_student_typed('c')))
```

The SCT above tests that the student typed 'c' in the ORELSE part of the inner `if` expression.
In parts, this looks like..

```{python}
BODY1 if TEST1 else (ORELSE1 = BODY2 if TEST2 else ORELSE2)
```
