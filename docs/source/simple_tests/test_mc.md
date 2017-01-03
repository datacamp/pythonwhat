test_mc
-------

```eval_rst
.. automodule:: pythonwhat.test_funcs.test_mc
    :members:
```

    test_mc(correct, msgs)

Multiple choice exercises are straightforward to test. Use `test_mc()` to provide tailored feedback for both the incorrect options, as the correct option. Below is the code for a multiple choice exercise example, with an SCT that uses `test_mc`:

    --- type:MultipleChoiceExercise lang:python xp:50 skills:2
    ## The author of Python
    
    Who is the author of the Python programming language?
    
    *** =instructions
    - Roy Co
    - Ronald McDonald
    - Guido van Rossum
    
    *** =hint
    Just google it!
    
    *** =sct
    ```{python}
    test_mc(correct = 3, 
            msgs = ["That's someone who makes soups.",
                    "That's a clown who likes burgers.",
                    "Correct! Head over to the next exercise!"])
    ```

The first argument of `test_mc()`, `correct`, should be the number of the correct answer in this list. Here, the correct answer is Guido van Rossum, corresponding to 3. The `msgs` argument should be a list of strings with a length equal to the number of options. We encourage you to provide feedback messages that are informative and tailored to the (incorrect) option that people selected. Make sure to correctly order the feedback message such that it corresponds to the possible answers that are listed in the instructions tab. Notice that there's no need for `success_msg()` in multiple choice exercises, as you have to specify the success message inside `test_mc()`, along with the feedback for incorrect options.
