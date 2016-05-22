
# pythonwhat Module


# pythonwhat.Reporter Module
> This file holds the reporter class.



## pythonwhat.Reporter.Reporter Objects



##### `__init__(self)` 



##### `active_reporter = None` 


##### `allow_errors(self)` 



##### `do_test(self, test_object)` 

> Do test.
> 
>         Execute a given test, unless some previous test has failed. If the test has failed,
>         the state of the reporter changes and the feedback is kept.



##### `do_tests(self, test_objects)` 

> Do multiple tests.
> 
>         Execute an array of tests.



##### `fail(self, failure_msg)` 



##### `get_tags(self)` 



##### `inc_correct_steps_to(self, correct_steps)` 



##### `reject_errors(self)` 



##### `set_success_msg(self, success_msg)` 



##### `set_tag(self, key, value)` 



# pythonwhat.State Module


## pythonwhat.State.State Objects



##### `__init__(self, student_code, solution_code, pre_exercise_code, student_env, solution_env, raw_student_output)` 



##### `active_state = None` 


##### `add_pre_exercise_code(self, pre_exercise_code)` 



##### `add_raw_student_output(self, raw_student_output)` 



##### `add_solution_code(self, solution_code)` 



##### `add_solution_env(self, solution_env)` 



##### `add_student_code(self, student_code)` 



##### `add_student_env(self, student_env)` 



##### `extract_for_calls(self)` 



##### `extract_function_calls(self)` 



##### `extract_if_calls(self)` 



##### `extract_imports(self)` 



##### `extract_operators(self)` 



##### `extract_while_calls(self)` 



##### `get_subcode(subtree, full_code)` 

> Extract code subtree.
> 
>         Extract all the code belonging to a subtree of the code.



##### `parse_code(self)` 



##### `set_active_state(to_state)` 



##### `to_child_state(self, student_subtree, solution_subtree)` 

> Dive into nested tree.
> 
>         Set the current state as a state with a subtree of this syntax tree as
>         student tree and solution tree. This is necessary when testing if statements or
>         for loops for example.



##### `to_parent_state(self)` 



# pythonwhat.Test Module


## pythonwhat.Test.BiggerTest Objects



##### `__init__(self, obj1, obj2, failure_msg)` 

> Initialize with two objects.
> 
> Args:
>         obj1 (str): The first object, obj1 will be set to this.
>         obj2 (str): The second object, obj2 will be set to this.
>         failure_msg (str): The failure message will be set to this.



##### `specific_test(self)` 

> Perform the actual test. result is set to False if the objects differ, True otherwise.



## pythonwhat.Test.CollectionContainsTest Objects



##### `__init__(self, obj, coll, failure_msg)` 



##### `specific_test(self)` 



## pythonwhat.Test.DefinedTest Objects



##### `__init__(self, obj, coll, failure_msg)` 

> Initialize the defined test.
> 
> Args:
>         obj (str): Value to which obj will be set.
>         coll (list/dict/set): The coll will be set to this.
>         failure_msg (str): The failure message will be set to this.



##### `specific_test(self)` 

> Perform the actual test. Result is True if obj is in coll, False otherwise.



## pythonwhat.Test.EnvironmentTest Objects



##### `__init__(self, obj, student_env, solution_env, failure_msg)` 

> Initialize with a student and solution environment.
> 
> Args:
>         student_env (dict): The student environment will be set to this.
>         solution_env (dict): The solution environment will be set to this.
>         failure_msg (str): The failure message will be set to this.



## pythonwhat.Test.EqualEnvironmentTest Objects



##### `__init__(self, obj, student_env, solution_env, failure_msg)` 

> Initialize with an object, student and solution environment.
> 
> Args:
>         obj (str): The variable name, obj will be set to this.
>         student_env (dict): The student environment will be set to this.
>         solution_env (dict): The solution environment will be set to this.
>         failure_msg (str): The failure message will be set to this.



##### `specific_test(self)` 

> Perform the actual test. result is set to False if the variables differ, True otherwise.



## pythonwhat.Test.EqualTest Objects



##### `__init__(self, obj1, obj2, failure_msg)` 

> Initialize with two objects.
> 
> Args:
>         obj1 (str): The first object, obj1 will be set to this.
>         obj2 (str): The second object, obj2 will be set to this.
>         failure_msg (str): The failure message will be set to this.



##### `specific_test(self)` 

> Perform the actual test. result is set to False if the objects differ, True otherwise.



## pythonwhat.Test.EquivalentEnvironmentTest Objects



##### `__init__(self, obj, student_env, solution_env, failure_msg)` 

> Initialize with an object, student and solution environment.
> 
> Args:
>         obj (str): The variable name, obj will be set to this.
>         student_env (dict): The student environment will be set to this.
>         solution_env (dict): The solution environment will be set to this.
>         failure_msg (str): The failure message will be set to this.



##### `specific_test(self)` 



## pythonwhat.Test.EquivalentTest Objects



##### `__init__(self, obj1, obj2, failure_msg)` 

> Initialize with two objects.
> 
> Args:
>         obj1 (str): The first object, obj1 will be set to this.
>         obj2 (str): The second object, obj2 will be set to this.
>         failure_msg (str): The failure message will be set to this.



##### `specific_test(self)` 

> Perform the actual test. result is set to False if the difference between the objects is
> more than 0.5e-8, True otherwise.



## pythonwhat.Test.StringContainsTest Objects



##### `__init__(self, string, search_string, pattern, failure_msg)` 

> Initialize with a string to look for, a string to search and whether or not to look for a pattern.
> 
> Args:
>         string (regex/str):  The string to look for will be set to this.
>         search_string (str): The string to search in will be set to this.
>         pattern (bool): The pattern boolean will be set to this.
>         failure_msg (str): The failure message will be set to this.



##### `specific_test(self)` 

> Perform the actual test. result will be True if string is found (whether or not with a pattern),
> False otherwise.



## pythonwhat.Test.Test Objects



##### `__init__(self, failure_msg)` 

> Initialize the standard test.
> 
> Args:
>         failure_msg (str): The failure message will be set to this.



##### `feedback(self)` 



##### `specific_test(self)` 

> Perform the actual test. For the standard test, result will be set to False.



##### `test(self)` 

> Wrapper around specific tests. Tests only get one chance.



# pythonwhat.feedback Module


## pythonwhat.feedback.FeedbackMessage Objects



##### `__init__(self, message_string)` 



##### `add_information(self, key, value)` 



##### `append(self, message_string)` 



##### `cond_append(self, cond, message_string)` 



##### `generateString(self)` 



##### `remove_information(self, key)` 



##### `replaceConditionalTags(message_string, information)` 



##### `replaceRegularTags(message_string, information)` 



##### `set(self, message_string)` 



##### `set_information(self, key, value)` 



# pythonwhat.parsing Module


## pythonwhat.parsing.BoolParser Objects



##### `__init__(self)` 

> Initialize the parser and its attributes.



## pythonwhat.parsing.FindLastLineParser Objects



##### `__init__(self)` 



##### `generic_visit(self, node)` 



## pythonwhat.parsing.ForParser Objects



##### `__init__(self)` 

> Initialize the parser and its attributes.



##### `visit_For(self, node)` 

> This function is called when a For node is encountered when traversing the tree.
> 
> Args:
>     node (ast.For): The node which is visited.



## pythonwhat.parsing.FunctionParser Objects



##### `__init__(self)` 

> Initialize the parser and its attributes.



##### `visit_Assign(self, node)` 



##### `visit_Attribute(self, node)` 

> This function is called when a Attribute node is encountered when traversing the tree.
> 
> Args:
>     node (ast.Attribute): The node which is visited.



##### `visit_BinOp(self, node)` 



##### `visit_Call(self, node)` 

> This function is called when a Call node is encountered when traversing the tree.
> 
> Args:
>     node (ast.Call): The node which is visited.



##### `visit_Expr(self, node)` 

> This function is called when a Expr node is encountered when traversing the tree.
> 
> Args:
>     node (ast.Expr): The node which is visited.



##### `visit_Import(self, node)` 



##### `visit_ImportFrom(self, node)` 



##### `visit_Name(self, node)` 

> This function is called when a Name node is encountered when traversing the tree.
> 
> Args:
>     node (ast.Name): The node which is visited.



##### `visit_UnaryOp(self, node)` 



## pythonwhat.parsing.IfParser Objects



##### `__init__(self)` 

> Initialize the parser and its attributes.



##### `visit_If(self, node)` 

> This function is called when a If node is encountered when traversing the tree.
> 
> Args:
>     node (ast.If): The node which is visited.



## pythonwhat.parsing.ImportParser Objects



##### `__init__(self)` 

> Initialize the parser and its attributes.



##### `visit_Import(self, node)` 

> This function is called when an Import node is encountered when traversing the tree.
> 
> Args:
>     node (ast.Import): The node which is visited.



##### `visit_ImportFrom(self, node)` 

> This function is called when an ImportFrom node is encountered when traversing the tree.
> 
> Args:
>     node (ast.ImportFrom): The node which is visited.



## pythonwhat.parsing.OperatorParser Objects



##### `__init__(self)` 

> Initialize the parser and its attributes.



##### `O_MAP` 


##### `visit_Assign(self, node)` 

> This function is called when a Assign node is encountered when traversing the tree.
> 
> Args:
>     node (ast.Assign): The node which is visited.



##### `visit_BinOp(self, node)` 

> This function is called when a BinOp node is encountered when traversing the tree.
> 
> Args:
>     node (ast.BinOp): The node which is visited.



##### `visit_Call(self, node)` 

> This function is called when a Call node is encountered when traversing the tree.
> 
> Args:
>     node (ast.Call): The node which is visited.



##### `visit_Expr(self, node)` 

> This function is called when a Expr node is encountered when traversing the tree.
> 
> Args:
>     node (ast.Expr): The node which is visited.



##### `visit_Num(self, node)` 

> This function is called when a Num node is encountered when traversing the tree.
> 
> Args:
>     node (ast.Num): The node which is visited.



##### `visit_UnaryOp(self, node)` 

> This function is called when a UnaryOp node is encountered when traversing the tree.
> 
> Args:
>     node (ast.UnaryOp): The node which is visited.



## pythonwhat.parsing.Parser Objects



##### `generic_visit(self, node)` 

> This function is called when all other nodes are encountered when traversing the tree.
> When inheriting form this standard parser, this function will make the parser ignore
> all nodes that are not relevant to build its data structures.
> 
> Args:
>     node (ast.Node): The node which is visited.



##### `visit_Expression(self, node)` 

> This function is called when a Expression node is encountered when traversing the tree.
> 
> Args:
>     node (ast.Expression): The node which is visited.



##### `visit_Module(self, node)` 

> This function is called when a Module node is encountered when traversing the tree.
> 
> Args:
>     node (ast.Module): The node which is visited.



## pythonwhat.parsing.WhileParser Objects



##### `__init__(self)` 



##### `visit_While(self, node)` 



# pythonwhat.test_exercise Module


## Functions

##### `allow_errors()` 



##### `success_msg(message)` 

> Set the succes message of the sct. This message will be the feedback if all tests pass.
> Args:
>         message (str): A string containing the feedback message.



##### `test_exercise(sct, student_code, solution_code, pre_exercise_code, student_environment, solution_environment, raw_student_output, ex_type, error)` 

> Point of interaction with the Python backend.
> Args:
>         sct (str): The solution corectness test as a string of code.
>         student_code (str): The code which is entered by the student.
>         solution_code (str): The code which is in the solution.
>         pre_exercise_code (str): The code which is executed pre exercise.
>         student_environment (dict): A dictionary representing the ending environment of the student's program.
>         solution_environment (dict): A dictionary representing the ending environment of the solution.
>         raw_student_output (str): The output which is given by executing the student's program.
>         ex_type (str): The type of the exercise.
>         error (tuple): A tuple with some information on possible errors.
> Returns:
>         dict: Returns dict with correct - whether the SCT passed, message - the feedback message and
>           tags - the tags belonging to the SCT execution.



##### `to_html(msg)` 



# pythonwhat.test_expression_output Module


## Functions

##### `capture_output(*args, **kwds)` 



##### `test_expression_output(extra_env=None, context_vals=None, incorrect_msg=None, eq_condition='equal', pre_code=None, keep_objs_in_env=None)` 

> Test output of expression.
> 
>     The code of the student is ran in the active state and the output it generates is
>     compared with the code of the solution. This can be used in nested pythonwhat calls
>     like test_if_else. In these kind of calls, the code of the active state is set to
>     the code in a part of the sub statement (e.g. the body of an if statement). It
>     has various parameters to control the execution of the (sub)expression.
> 
>     Example:
>       student_code
>         | ``a = 12``
>         | ``if a > 3:``
>         | ``    print('test %d' % a)``
>       solution_code
>         | ``a = 4``
>         | ``if a > 3:``
>         | ``    print('test %d' % a)``
>       sct
>         | ``test_if_else(1,``
>         | ``             body = lambda: test_expression_output(extra_env = { 'a': 5 }``
>         | ``                                                   incorrect_msg = "Print out the correct things"))``
>       This SCT will pass as the subexpression will output 'test 5' in both student as solution environment,
>       since the extra environment sets `a` to 5.
> 
>     Args:
>         extra_env (dict): set variables to the extra environment. They will update the student
>           and solution environment in the active state before the student/solution code in the active
>           state is ran. This argument should contain a dictionary with the keys the names of
>           the variables you want to set, and the values are the values of these variables.
>         context_vals (list): set variables which are bound in a for loop to certain values. This argument is
>           only useful if you use the function in a test_for_loop. It contains a list with the values
>           of the bound variables.
>         incorrect_msg (str): feedback message if the output of the expression in the solution doesn't match
>           the one of the student. This feedback message will be expanded if it is used in the context of
>           another test function, like test_if_else.
>         eq_condition (str): the condition which is checked on the eval of the group. Can be "equal" --
>           meaning that the operators have to evaluate to exactly the same value, or "equivalent" -- which
>           can be used when you expect an integer and the result can differ slightly. Defaults to "equal".
>         pre_code (str): the code in string form that should be executed before the expression is executed.
>           This is the ideal place to set a random seed, for example.
>         keep_obj_in_env (list()): a list of variable names that should be hold in the copied environment where
>           the expression is evaluated. All primitive types are copied automatically, other objects have to
>           be passed explicitely.



# pythonwhat.test_expression_result Module


## Functions

##### `test_expression_result(extra_env=None, context_vals=None, incorrect_msg=None, eq_condition='equal', expr_code=None, pre_code=None, keep_objs_in_env=None)` 

> Test result of expression.
> 
>     The code of the student is ran in the active state and the result of the evaluation is
>     compared with the result of the solution. This can be used in nested pythonwhat calls
>     like test_if_else. In these kind of calls, the code of the active state is set to
>     the code in a part of the sub statement (e.g. the condition of an if statement). It
>     has various parameters to control the execution of the (sub)expression.
> 
>     Example:
>       student_code
>         | ``a = 12``
>         | ``if a > 3:``
>         | ``    print('test %d' % a)``
>       solution_code
>         | ``a = 4``
>         | ``b = 5``
>         | ``if (a + 1) > (b - 1):``
>         | ``    print('test %d' % a)``
>       sct
>         | ``test_if_else(1,``
>         | ``             test = lambda: test_expression_result(extra_env = { 'a': 3 }``
>         | ``                                                   incorrect_msg = "Test if `a` > 3"))``
>       This SCT will pass as the condition in the student's code (`a > 3`) will evaluate to the
>       same value as the code in the solution code (`(a + 1) > (b - 1)`), with value of `a` set
>       to `3`.
> 
>     Args:
>         extra_env (dict): set variables to the extra environment. They will update the student
>           and solution environment in the active state before the student/solution code in the active
>           state is ran. This argument should contain a dictionary with the keys the names of
>           the variables you want to set, and the values are the values of these variables.
>         context_vals (list): set variables which are bound in a for loop to certain values. This argument is
>           only useful if you use the function in a test_for_loop. It contains a list with the values
>           of the bound variables.
>         incorrect_msg (str): feedback message if the result of the expression in the solution doesn't match
>           the one of the student. This feedback message will be expanded if it is used in the context of
>           another test function, like test_if_else.
>         eq_condition (str): the condition which is checked on the eval of the group. Can be "equal" --
>           meaning that the operators have to evaluate to exactly the same value, or "equivalent" -- which
>           can be used when you expect an integer and the result can differ slightly. Defaults to "equal".
>         expr_code (str): if this variable is not None, the expression in the studeont/solution code will not
>           be ran. Instead, the given piece of code will be ran in the student as well as the solution environment
>           and the result will be compared.
>         pre_code (str): the code in string form that should be executed before the expression is executed.
>           This is the ideal place to set a random seed, for example.
>         keep_obj_in_env (list()): a list of variable names that should be hold in the copied environment where
>           the expression is evaluated. All primitive types are copied automatically, other objects have to
>           be passed explicitely.



# pythonwhat.test_for_loop Module


## Functions

##### `test_for_loop(index=1, for_iter=None, body=None, orelse=None, expand_message=True)` 

> Test parts of the for loop.
> 
>     This test function will allow you to extract parts of a specific for loop and perform a set of tests
>     specifically on these parts. A for loop consists of two parts: the sequence, `for_iter`, which is the
>     values over which are looped, and the `body`. A for loop can have a else part as well, `orelse`, but
>     this is almost never used.
> 
>         ``for i in range(10):``
>         ``    print(i)``
> 
>     Has `range(10)` as the sequence and `print(i)` as the body.
> 
>     Example:
>       student_code
>         | ``for i in range(10):``
>         | ``    print(i)``
>       solution_code
>         | ``for n in range(10):``
>         | ``    print(n)``
>       sct
>         | ``test_for_loop(1,``
>         | ``              for_iter = lamdba: test_function("range"),``
>         | ``              body = lambda: test_expression_output(context_val = [5])``
>       This SCT will evaluate to TRUE as the function `"range"` is used in the sequence and the function
>       `test_exression_output()` will pass on the body code.
> 
>     Args:
>       index (int): index of the function call to be checked. Defaults to 1.
>       for_iter: this argument holds the part of code that will be ran to check the sequence of the for loop.
>         It should be passed as a lambda expression or a function definition. The functions that are ran should
>         be other pythonwhat test functions, and they will be tested specifically on only the sequence part of
>         the for loop.
>       body: this argument holds the part of code that will be ran to check the body of the for loop.
>         It should be passed as a lambda expression or a function definition. The functions that are ran should
>         be other pythonwhat test functions, and they will be tested specifically on only the body of
>         the for loop.
>       orelse: this argument holds the part of code that will be ran to check the else part of the for loop.
>         It should be passed as a lambda expression or a function definition. The functions that are ran should
>         be other pythonwhat test functions, and they will be tested specifically on only the else part of
>         the for loop.
>       expand_message (bool): if true, feedback messages will be expanded with `in the ___ of the for loop on
>         line ___`. Defaults to True. If False, `test_for_loop()` will generate no extra feedback.



# pythonwhat.test_function Module


## Functions

##### `construct_incorrect_msg(nb_call)` 



##### `ordinal(n)` 



##### `test_function(name, index=1, args=None, keywords=None, eq_condition='equal', do_eval=True, not_called_msg=None, incorrect_msg=None)` 

> Test if function calls match.
> 
>     This function compares a function call in the student's code with the corresponding one in the solution
>     code. It will cause the reporter to fail if the corresponding calls do not match. The fail message
>     that is returned will depend on the sort of fail.
> 
>     Example:
>       student_code
>         | ``import numpy as np``
>         | ``np.mean([1,2,3])``
>         | ``np.std([2,3,4])``
>       solution_code
>         | ``import numpy``
>         | ``numpy.mean([1,2,3], axis = 0)``
>         | ``numpy.std([4,5,6])``
>       sct
>         | ``test_function("numpy.mean", index = 1, keywords = [])``: pass.
>         | ``test_function("numpy.mean", index = 1)``: fails with "Your operation at line 2 is missing a `*` operation".
>         | ``test_function(index = 1, incorrect_op_msg = "Use the correct operators")``: fails with "Use the correct operators".
>         | ``test_function(index = 1, used = [], incorrect_result_msg = "Incorrect result")``: fails with "Incorrect result".
> 
>     Args:
>         name (str): the name of the function to be tested.
>         index (int): index of the function call to be checked. Defaults to 1.
>         args (list(int)): the indices of the positional arguments that have to be checked. If it is set to
>           None, all positional arguments which are in the solution will be checked.
>         keywords (list(str)): the indices of the keyword arguments that have to be checked. If it is set to
>           None, all keyword arguments which are in the solution will be checked.
>         eq_condition (str): The condition which is checked on the eval of the group. Can be "equal" --
>           meaning that the operators have to evaluate to exactly the same value, or "equivalent" -- which
>           can be used when you expect an integer and the result can differ slightly. Defaults to "equal".
>         do_eval (bool): Boolean representing whether the group should be evaluated and compared or not.
>           Defaults to True.
>         not_called_msg (str): feedback message if the function is not called.
>         incorret_msg (str): feedback message if the arguments of the function in the solution doesn't match
>           the one of the student.
> 
>     Raises:
>       NameError: the eq_condition you passed is not "equal" or "equivalent".
>       NameError: function is not called in the solution



# pythonwhat.test_if_else Module


## Functions

##### `test_if_else(index=1, test=None, body=None, orelse=None, expand_message=True)` 

> Test parts of the if statement.
> 
>     This test function will allow you to extract parts of a specific if statement and perform a set of tests
>     specifically on these parts. A for loop consists of three potential parts: the condition test, `test`,
>     which specifies the condition of the if statement, the `body`, which is what's executed if the condition is
>     True and a else part, `orelse`, which will be executed if the condition is not True.
> 
>         ``if 5 == 3:``
>         ``    print("success")``
>         ``else:``
>         ``    print("fail")``
> 
> 
>     Has `5 == 3` as the condition test, `print("success")` as the body and `print("fail")` as the else part.
> 
>     Example:
>       student_code
>         | ``a = 12``
>         | ``if a > 3:``
>         | ``    print('test %d' % a)``
>       solution_code
>         | ``a = 4``
>         | ``if a > 3:``
>         | ``    print('test %d' % a)``
>       sct
>         | ``test_if_else(1,``
>         | ``             body = lambda: test_expression_output(extra_env = { 'a': 5 }``
>         | ``                                                   incorrect_msg = "Print out the correct things"))``
>       This SCT will pass as `test_expression_output()` is ran on the body of the if statement and it will output
>       the same thing in the solution as in the student code.
> 
>     Args:
>       index (int): index of the function call to be checked. Defaults to 1.
>       test: this argument holds the part of code that will be ran to check the condition test of the if statement.
>         It should be passed as a lambda expression or a function definition. The functions that are ran should
>         be other pythonwhat test functions, and they will be tested specifically on only the condition test of
>         the if statement.
>       body: this argument holds the part of code that will be ran to check the body of the if statement.
>         It should be passed as a lambda expression or a function definition. The functions that are ran should
>         be other pythonwhat test functions, and they will be tested specifically on only the body of
>         the if statement.
>       orelse: this argument holds the part of code that will be ran to check the else part of the if statement.
>         It should be passed as a lambda expression or a function definition. The functions that are ran should
>         be other pythonwhat test functions, and they will be tested specifically on only the else part of
>         the if statement.
>       expand_message (bool): if true, feedback messages will be expanded with `in the ___ of the if statement on
>         line ___`. Defaults to True. If False, `test_if_else()` will generate no extra feedback.



# pythonwhat.test_import Module


## Functions

##### `test_import(name, same_as=True, not_imported_msg=None, incorrect_as_msg=None)` 

> Test import.
> 
>     Test whether an import statement is used the same in the student's environment as in the solution
>     environment.
> 
>     Example:
>       student_code
>         | ``import numpy as np``
>         | ``import pandas as pa``
>       solution_code
>         | ``import numpy as np``
>         | ``import pandas as pd``
>       sct
>         | ``test_import("numpy")``: passes
>         | ``test_import("pandas")``: fails
>         | ``test_import("pandas", same_as = False)``: passes
> 
>     Args:
>         name (str): the name of the package that has to be checked.
>         same_as (bool): if false, the alias of the package doesn't have to be the same. Defaults to True.
>         not_imported_msg (str): feedback message when the package is not imported.
>         incorrect_as_msg (str): feedback message if the alias is wrong.



# pythonwhat.test_mc Module


## Data
- `MC_VAR_NAME = 'selected_option'` 

## Functions

##### `test_mc(correct, msgs)` 

> Test multiple choice exercise.
> 
>     Test for a MultipleChoiceExercise. The correct answer (as an integer) and feedback messages
>     are passed to this function.
> 
>     Args:
>       correct (int): the index of the correct answer (should be an instruction). Starts at 1.
>       msgs (list(str)): a list containing all feedback messages belonging to each choice of the
>         student. The list should have the same length as the number of instructions.



# pythonwhat.test_object Module


## Functions

##### `build_strings(undefined_msg, incorrect_msg, name)` 



##### `test_object(name, eq_condition='equal', do_eval=True, undefined_msg=None, incorrect_msg=None)` 

> Test object.
> 
>     The value of an object in the ending environment is compared in the student's environment and the
>     solution environment.
> 
>     Example:
>       student_code
>         | ``a = 1``
>         | ``b = 5``
>       solution_code
>         | ``a = 1``
>         | ``b = 2``
>       sct
>         | ``test_object("a")``: passes
>         | ``test_object("b")``: fails
> 
>     Args:
>         name (str): the name of the object which value has to be checked.
>         eq_condition (str): the condition which is checked on the eval of the object. Can be "equal" --
>           meaning that the operators have to evaluate to exactly the same value, or "equivalent" -- which
>           can be used when you expect an integer and the result can differ slightly. Defaults to "equal".
>         do_eval (bool): if False, the object will only be checked for existence. Defaults to True.
>         undefined_msg (str): feedback message when the object is not defined
>         incorrect_msg (str): feedback message if the value of the object in the solution environment doesn't match
>           the one in the student environment.



# pythonwhat.test_object_after_expression Module


## Functions

##### `build_strings(undefined_msg, incorrect_msg, name)` 



##### `test_object_after_expression(name, extra_env=None, context_vals=None, undefined_msg=None, incorrect_msg=None, eq_condition='equal', pre_code=None, keep_objs_in_env=None)` 

> Test object after expression.
> 
>     The code of the student is ran in the active state and the the value of the given object is
>     compared with the value of that object in the solution. This can be used in nested pythonwhat calls
>     like test_for_loop. In these kind of calls, the code of the active state is set to
>     the code in a part of the sub statement (e.g. the body of a for loop). It has various
>     parameters to control the execution of the (sub)expression. This test function is ideal to check if
>     a value is updated correctly in the body of a for loop.
> 
>     Example:
>       student_code
>         | ``count = 1``
>         | ``for i in range(100):``
>         | ``    count = count + i``
>       solution_code
>         | ``count = 15``
>         | ``for n in range(30):``
>         | ``    count = count + n``
>       sct
>         | ``test_for_loop(1,``
>         | ``              body = lambda: test_object_after_expression("count",``
>         | ``                                                          extra_env = { 'count': 20 },``
>         | ``                                                          contex_vals = [ 10 ])``
>       This SCT will pass as the value of `count` is updated identically in the body of the for loop in the
>       student code and solution code.
> 
>     Args:
>         name (str): the name of the object which value has to be checked after evaluation of the expression.
>         extra_env (dict): set variables to the extra environment. They will update the student
>           and solution environment in the active state before the student/solution code in the active
>           state is ran. This argument should contain a dictionary with the keys the names of
>           the variables you want to set, and the values are the values of these variables.
>         context_vals (list): set variables which are bound in a for loop to certain values. This argument is
>           only useful if you use the function in a test_for_loop. It contains a list with the values
>           of the bound variables.
>         incorrect_msg (str): feedback message if the value of the object in the solution environment doesn't match
>           the one in the student environment. This feedback message will be expanded if it is used in the context of
>           another test function, like test_for_loop.
>         eq_condition (str): the condition which is checked on the eval of the object. Can be "equal" --
>           meaning that the operators have to evaluate to exactly the same value, or "equivalent" -- which
>           can be used when you expect an integer and the result can differ slightly. Defaults to "equal".
>         expr_code (str): if this variable is not None, the expression in the studeont/solution code will not
>           be ran. Instead, the given piece of code will be ran in the student as well as the solution environment
>           and the result will be compared.
>         pre_code (str): the code in string form that should be executed before the expression is executed.
>           This is the ideal place to set a random seed, for example.
>         keep_obj_in_env (list()): a list of variable names that should be hold in the copied environment where
>           the expression is evaluated. All primitive types are copied automatically, other objects have to
>           be passed explicitely.



# pythonwhat.test_operator Module


## Functions

##### `test_operator(index=1, eq_condition='equal', used=None, do_eval=True, not_found_msg=None, incorrect_op_msg=None, incorrect_result_msg=None)` 

> Test if operator groups match.
> 
>     This function compares an operator group in the student's code with the corresponding one in the solution
>     code. It will cause the reporter to fail if the corresponding operators do not match. The fail message
>     that is returned will depend on the sort of fail. We say that one operator group correpsonds to a group of
>     operators that is evaluated to one value (e.g. 3 + 5 * (1/3)).
> 
>     Example:
>       student_code
>         | ``1 + 5 * (3+5)``
>         | ``1 + 1 * 238``
>       solution_code
>         | ``3.1415 + 5``
>         | ``1 + 238``
>       sct
>         | ``test_operator(index = 2, used = ["+"])``: pass.
>         | ``test_operator(index = 2)``: fails with "Your operation at line 2 is missing a `*` operation".
>         | ``test_operator(index = 1, incorrect_op_msg = "Use the correct operators")``: fails with "Use the correct operators".
>         | ``test_operator(index = 1, used = [], incorrect_result_msg = "Incorrect result")``: fails with "Incorrect result".
> 
>     Args:
>         index (int): Index of the operator group to be checked. Defaults to 1.
>         eq_condition (str): The condition which is checked on the eval of the group. Can be "equal" --
>           meaning that the operators have to evaluate to exactly the same value, or "equivalent" -- which
>           can be used when you expect an integer and the result can differ slightly. Defaults to "equal".
>         used(List[str]): A list of operators that have to be in the group. Valid operators are: "+", "-",
>           "*", "/", "%", "**", "<<", ">>", "|", "^", "&" and "//". If the list is None, operators that are
>           in the group in the solution have to be in the student code. Defaults to None.
>         do_eval (bool): Boolean representing whether the group should be evaluated and compared or not.
>           Defaults to True.
>         not_found_msg (str): Feedback message if not enough operators groups are found in the student's code.
>         incorrect_op_msg (str): Feedback message if the wrong operators are used in the student's code.
>         incorrect_result_msg (str): Feedback message if the operator group evaluates to the wrong result in
>           the student's code.
> 
>     Raises:
>       NameError: the eq_condition you passed is not "equal" or "equivalent".
>       IndexError: not enough operation groups in the solution environment.



# pythonwhat.test_output_contains Module


## Functions

##### `test_output_contains(text, pattern=True, no_output_msg=None)` 

> Test the output.
> 
>     Tests if the output contains a (pattern of) text.
> 
>     Args:
>       text (str): the text that is searched for
>       pattern (bool): if True, the text is treated as a pattern. If False, it is treated as plain text.
>         Defaults to False.
>       no_output_msg (str): feedback message to be displayed if the output is not found.



# pythonwhat.test_student_typed Module


## Functions

##### `test_student_typed(text, pattern=True, not_typed_msg=None)` 

> Test the student code.
> 
>     Tests if the student typed a (pattern of) text.
> 
>     Args:
>       text (str): the text that is searched for
>       pattern (bool): if True, the text is treated as a pattern. If False, it is treated as plain text.
>         Defaults to False.
>       not_typed_msg (str): feedback message to be displayed if the student did not type the text.



# pythonwhat.test_while_loop Module


## Functions

##### `test_while_loop(index=1, test=None, body=None, orelse=None, expand_message=True)` 

> Test parts of the for loop.
> 
>     This test function will allow you to extract parts of a specific for loop and perform a set of tests
>     specifically on these parts. A for loop consists of two parts: the sequence, `for_iter`, which is the
>     values over which are looped, and the `body`. A for loop can have a else part as well, `orelse`, but
>     this is almost never used.
> 
>         ``for i in range(10):``
>         ``    print(i)``
> 
>     Has `range(10)` as the sequence and `print(i)` as the body.
> 
>     Example:
>       student_code
>         | ``for i in range(10):``
>         | ``    print(i)``
>       solution_code
>         | ``for n in range(10):``
>         | ``    print(n)``
>       sct
>         | ``test_for_loop(1,``
>         | ``              for_iter = lamdba: test_function("range"),``
>         | ``              body = lambda: test_expression_output(context_val = [5])``
>       This SCT will evaluate to TRUE as the function `"range"` is used in the sequence and the function
>       `test_exression_output()` will pass on the body code.
> 
>     Args:
>       index (int): index of the function call to be checked. Defaults to 1.
>       for_iter: this argument holds the part of code that will be ran to check the sequence of the for loop.
>         It should be passed as a lambda expression or a function definition. The functions that are ran should
>         be other pythonwhat test functions, and they will be tested specifically on only the sequence part of
>         the for loop.
>       body: this argument holds the part of code that will be ran to check the body of the for loop.
>         It should be passed as a lambda expression or a function definition. The functions that are ran should
>         be other pythonwhat test functions, and they will be tested specifically on only the body of
>         the for loop.
>       orelse: this argument holds the part of code that will be ran to check the else part of the for loop.
>         It should be passed as a lambda expression or a function definition. The functions that are ran should
>         be other pythonwhat test functions, and they will be tested specifically on only the else part of
>         the for loop.
>       expand_message (bool): if true, feedback messages will be expanded with `in the ___ of the for loop on
>         line ___`. Defaults to True. If False, `test_for_loop()` will generate no extra feedback.



# pythonwhat.utils Module


## Functions

##### `copy_env(env, keep_objs=None)` 



##### `shorten_str(text, to_chars=100)` 


