parts_cheatsheet
----------------

### test_list_comp

```{python}
[BODY for i in COMP_ITER if IFS[0] if IFS[1]]
```

### test_dict_comp

```{python}
{ KEY : VALUE for k, v in COMP_ITER if IFS[0] if IFS[1] }
```
### test_generator_exp

```{python}
(BODY for i in COMP_ITER if IFS[0] if IFS[1])
```

### test_for_loop
```{python}
for i in FOR_ITER:
    BODY
else:
    ORELSE
```

_yes, you can put an else statement at the end!_

### test_if_else

```{python}
if TEST:
    BODY
else:
    ORELSE
```

or, in the case of elif statements...

```{python}
if TEST:
    BODY
ORELSE
```

### test_lambda
```{python}
lambda x: BODY
```

### test_try_except

```{python}
try:
    BODY
except BaseException:
    HANDLERS['BaseException']
except:
    HANDLERS['all']
else: 
    ORELSE
finally:
    FINALBODY
```

### test_while

```{python}
while TEST:
    BODY
else:
    ORELSE
```

### test_with

```{python}
with CONTEXT_TEST as context_var:
    BODY
```

### test_function_definition

```{python}
def f(a, b):
    BODY
```
