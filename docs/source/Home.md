Home
====

pythonwhat?
-----------

A major part of DataCamp's interactive learning is centered around automated and meaningful feedback. When a student submits an incorrect answer, the system tells the student what he or she is doing wrong. This happens through so-called submission correctness tests, or SCTs. An SCT is a test script that compares the different steps in a student's submission to the ideal solution, and generates meaningful feedback along the way.

`pythonwhat` is a Python package that can help you write these SCTs for interactive Python exercises on DataCamp. It allows you to easily compare parts in the student's submission with the solution code. `pythonwhat` provides a bunch of functions to test object definitions, function calls, function definitions, for loops, while loops, and many more. `pythonwhat` automatically generates meaningful feedback that's specific to the student's mistake; you can also choose to override this feedback with custom messages.

Writing SCTs, for which `pythonwhat` is built, is only one part of creating DataCamp exercises. For general documentation on creating Python courses on DataCamp, visit the [Teach Documentation](https://www.datacamp.com/teach/documentation). To write SCTs for R exercises on DataCamp, have a look at [testwhat](https://github.com/datacamp/testwhat).

How does it work?
-----------------

When a student starts an exercise on DataCamp, a Python session is started and the `pre_exercise_code` (PEC) is run. This code, that the author specifies, initializes the Python workspace with data, loads relevant packages etc, such that students can start coding the essence of the topics treated. Next, a separate solution process is created, in which the same PEC and actual solution code, also coded by the author, is executed.

When a student submits an answer, his or her submission is executed and the output is shown in the IPython Shell. Then, the correctness of the submission is checked by executing the Submission Correctness Test, or SCT. Basically, your SCT is a Python script with calls to `pythonwhat` test functions. `pythonwhat` features a variety of functions to test a user's submission in different ways; examples are `test_object()`, `test_function()` and `test_output_contains()`. To do this properly, `pythonwhat` uses several resources:

- The student submission as text, to e.g. figure out which functions have been called.
- The solution code as text, to e.g. figure out whether the student called a particular function in the same way as it is called in the solution.
- The student process, where the student code is executed, to e.g. figure out whether a certain object was created.
- The solution process, where the solution code is executed, to e.g. figure out whether an object that the student created corresponds to the object that was created by the solution.
- The output that's generated when executing the student code, to e.g. figure out if the student printed out something.

If, during execution of the SCT, a test function notices a mistake, an appropriate feedback will be generated and presented to the student. It is always possible to override these feedback messages with your own messages. Defining custom feedback will make your SCTs longer and they may be error prone (typos, etc.), but they typically give the exercise a more natural and personalized feel.

If all test functions pass, a success message is presented to the student. `pytonwhat` has some messages in store from which it can choose randomly, but you can override this with the `success_msg()` function.

Overview
--------

To get started, make sure to check out the [Quickstart Guide](https://www.github.com/datacamp/pythonwhat/wiki/Quickstart_Guide).

To robustly test the equality of objects, and results of evaluations, it has to fetch the information from the respective processes, i.e. the student and solution processes. By default, this is done through a process of 'dilling' and 'undilling', but it's also possible to define your own converters to customize the way objects and results are compared. For more background on this, check out the [Processes article](https://github.com/datacamp/pythonwhat/wiki/Processes). For some more background on the principle of 'sub-SCTs', i.e. sets of tests to be called on a particular part or a particular state of a student's submission, have a look at the [Sub-SCTs article](https://github.com/datacamp/pythonwhat/wiki/Sub-SCTs).

The remainder of the wiki goes over every test function that `pythonwhat` features, explaining all arguments and covering different use cases. They will give you an idea of how, why and when to use them.

**Basic functions**

- Multiple choice exercises: [test_mc()](https://github.com/datacamp/pythonwhat/wiki/test_mc)
- What student typed: [test_student_typed()](https://github.com/datacamp/pythonwhat/wiki/test_student_typed)
- Which output is generated: [test_output_contains()](https://github.com/datacamp/pythonwhat/wiki/test_output_contains)
- Value of object: [test_object()](https://github.com/datacamp/pythonwhat/wiki/test_object)
- Usage of objects: [test_object_accessed()](https://github.com/datacamp/pythonwhat/wiki/tets_object_accessed)
- Usage of function: [test_function()](https://github.com/datacamp/pythonwhat/wiki/test_function)
- Usage of function, v2 (improved): [test_function_v2()](https://github.com/datacamp/pythonwhat/wiki/test_function_v2)
- Usage of operators: [test_operator()](https://github.com/datacamp/pythonwhat/wiki/test_operator)
- Package imports: [test_import()](https://github.com/datacamp/pythonwhat/wiki/test_import)

**Logic-inducing functions**

- If some tests fail, do other tests to pinpoint the problem: [test_correct()](https://www.github.com/datacamp/pythonwhat/wiki/test_correct)
- Specify several tests, only one of which should pass: [test_or()](https://www.github.com/datacamp/pythonwhat/wiki/test_or)

**Advanced functions**

- Value of data frame: [test_data_frame()](https://github.com/datacamp/pythonwhat/wiki/test_data_frame)
- Value of dictionary: [test_dictionary()](https://github.com/datacamp/pythonwhat/wiki/test_dictionary)
- If ... else ... constructs: [test_if_else()](https://github.com/datacamp/pythonwhat/wiki/test_if_else)
- For loops: [test_for_loop()](https://github.com/datacamp/pythonwhat/wiki/test_for_loop)
- While loops: [test_while_loop()](https://github.com/datacamp/pythonwhat/wiki/test_while_loop)
- Test value of object after expression: [test_object_after_expression()](https://github.com/datacamp/pythonwhat/wiki/test_object_after_expression)
- Test output of an expression: [test_expression_output()](https://github.com/datacamp/pythonwhat/wiki/test_expression_output)
- Test result of an expression: [test_expression_result()](https://github.com/datacamp/pythonwhat/wiki/test_expression_result)
- Context managers, the with statement: [test_with()](https://github.com/datacamp/pythonwhat/wiki/test_with)
- Test user-defined functions: [test_function_definition()](https://github.com/datacamp/pythonwhat/wiki/test_function_definition)
- Test lambda function definitions: [test_lambda_function()](https://github.com/datacamp/pythonwhat/wiki/test_lambda_function)
- Test comprehensions: [test_list_comp(), test_dict_comp() and test_generator_exp()](https://github.com/datacamp/pythonwhat/wiki/test_comprehension)
- Test try except blcoks: [test_try_except()](https://github.com/datacamp/pythonwhat/test_try_except)

All these functions are also documented inside the `pythonwhat` source code itself. The documentation there goes into the tiny details of all functions' implementations. Follow the steps in the README of this repository to generate a PDF version of the documentation.

For more full examples of SCTs for Python exercises on DataCamp, check out the [source files of the introduction to Python course](http://www.github.com/datacamp/courses-intro-to-python). In the chapter files there, you can can see the SCTs that have been written for several exercises.

To test your understanding of writing SCTs for Python exercises on the DataCamp platform, you can take the course [Writing SCTs with pythonwhat](https://www.datacamp.com/courses/writing-scts-with-pythonwhat) course.

After reading through this documentation, we hope writing SCTs for Python exercises on DataCamp becomes a painless experience. If this is not the case and you think improvements to `pythonwhat` and this documentation are possible, [please let us know](mailto:content-engineering@datacamp.com)!
