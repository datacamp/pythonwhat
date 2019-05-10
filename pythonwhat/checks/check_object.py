from pythonwhat.parsing import ObjectAssignmentParser
from pythonwhat.Test import (
    DefinedProcessTest,
    InstanceProcessTest,
    DefinedCollProcessTest,
)
from protowhat.Feedback import Feedback, InstructorError
from pythonwhat.tasks import (
    isDefinedInProcess,
    isInstanceInProcess,
    isDefinedCollInProcess,
)
from pythonwhat.checks.check_funcs import part_to_child
from pythonwhat.utils import v2_only
import pandas as pd
import ast


def check_object(state, index, missing_msg=None, expand_msg=None, typestr="variable"):
    """Check object existence (and equality)

    Check whether an object is defined in the student's process, and zoom in on its value in both
    student and solution process to inspect quality (with has_equal_value().

    In ``pythonbackend``, both the student's submission as well as the solution code are executed, in separate processes.
    ``check_object()`` looks at these processes and checks if the referenced object is available in the student process.
    Next, you can use ``has_equal_value()`` to check whether the objects in the student and solution process correspond.

    Args:
        index (str): the name of the object which value has to be checked.
        missing_msg (str): feedback message when the object is not defined in the student process.
        expand_msg (str): If specified, this overrides any messages that are prepended by previous SCT chains.

    :Example:

        Suppose you want the student to create a variable ``x``, equal to 15: ::

            x = 15

        The following SCT will verify this: ::

            Ex().check_object("x").has_equal_value()

        - ``check_object()`` will check if the variable ``x`` is defined in the student process.
        - ``has_equal_value()`` will check whether the value of ``x`` in the solution process is the same as in the student process.

        Note that ``has_equal_value()`` only looks at **end result** of a variable in the student process.
        In the example, how the object ``x`` came about in the student's submission, does not matter.
        This means that all of the following submission will also pass the above SCT: ::

            x = 15
            x = 12 + 3
            x = 3; x += 12

    :Example:

        As the previous example mentioned, ``has_equal_value()`` only looks at the **end result**. If your exercise is
        first initializing and object and further down the script is updating the object, you can only look at the final value!

        Suppose you want the student to initialize and populate a list `my_list` as follows: ::

            my_list = []
            for i in range(20):
                if i % 3 == 0:
                    my_list.append(i)

        There is no robust way to verify whether `my_list = [0]` was coded correctly in a separate way.
        The best SCT would look something like this: ::

            msg = "Have you correctly initialized `my_list`?"
            Ex().check_correct(
                check_object('my_list').has_equal_value(),
                multi(
                    # check initialization: [] or list()
                    check_or(
                        has_equal_ast(code = "[]", incorrect_msg = msg),
                        check_function('list')
                    ),
                    check_for_loop().multi(
                        check_iter().has_equal_value(),
                        check_body().check_if_else().multi(
                            check_test().multi(
                                set_context(2).has_equal_value(),
                                set_context(3).has_equal_value()
                            ),
                            check_body().set_context(3).\\
                                set_env(my_list = [0]).\\
                                has_equal_value(name = 'my_list')
                        )
                    )
                )
            )

        - ``check_correct()`` is used to robustly check whether ``my_list`` was built correctly.
        - If ``my_list`` is not correct, **both** the initialization and the population code are checked.

    :Example:

        Because checking object correctness incorrectly is such a common misconception, we're adding another example: ::

            import pandas as pd
            df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
            df['c'] = [7, 8, 9]

        The following SCT would be **wrong**, as it does not factor in the possibility that the 'add column ``c``' step could've been wrong: ::

            Ex().check_correct(
                check_object('df').has_equal_value(),
                check_function('pandas.DataFrame').check_args(0).has_equal_value()
            )

        The following SCT would be better, as it is specific to the steps: ::

            # verify the df = pd.DataFrame(...) step
            Ex().check_correct(
                check_df('df').multi(
                    check_keys('a').has_equal_value(),
                    check_keys('b').has_equal_value()
                ),
                check_function('pandas.DataFrame').check_args(0).has_equal_value()
            )

            # verify the df['c'] = [...] step
            Ex().check_df('df').check_keys('c').has_equal_value()

    :Example:

        pythonwhat compares the objects in the student and solution process with the ``==`` operator.
        For basic objects, this ``==`` is operator is properly implemented, so that the objects can be effectively compared.
        For more complex objects that are produced by third-party packages, however, it's possible that this equality operator is not implemented in a way you'd expect.
        Often, for these object types the ``==`` will compare the actual object instances: ::

            # pre exercise code
            class Number():
                def __init__(self, n):
                    self.n = n

            # solution
            x = Number(1)

            # sct that won't work
            Ex().check_object().has_equal_value()

            # sct
            Ex().check_object().has_equal_value(expr_code = 'x.n')

            # submissions that will pass this sct
            x = Number(1)
            x = Number(2 - 1)

        The basic SCT like in the previous example will notwork here.
        Notice how we used the ``expr_code`` argument to _override_ which value `has_equal_value()` is checking.
        Instead of checking whether `x` corresponds between student and solution process, it's now executing the expression ``x.n``
        and seeing if the result of running this expression in both student and solution process match.

    """

    # Only do the assertion if PYTHONWHAT_V2_ONLY is set to '1'
    if v2_only():
        extra_msg = "If you want to check the value of an object in e.g. a for loop, use `has_equal_value(name = 'my_obj')` instead."
        state.assert_root("check_object", extra_msg=extra_msg)

    if missing_msg is None:
        missing_msg = "Did you define the {{typestr}} `{{index}}` without errors?"

    if expand_msg is None:
        expand_msg = "Did you correctly define the {{typestr}} `{{index}}`? "

    if (
        not isDefinedInProcess(index, state.solution_process)
        and state.has_different_processes()
    ):
        raise InstructorError(
            "`check_object()` couldn't find object `%s` in the solution process."
            % index
        )

    append_message = {"msg": expand_msg, "kwargs": {"index": index, "typestr": typestr}}

    # create child state, using either parser output, or create part from name
    fallback = lambda: ObjectAssignmentParser.get_part(index)
    stu_part = state.ast_dispatcher.find("object_assignments", state.student_ast).get(
        index, fallback()
    )
    sol_part = state.ast_dispatcher.find("object_assignments", state.solution_ast).get(
        index, fallback()
    )

    # test object exists
    _msg = state.build_message(missing_msg, append_message["kwargs"])
    state.do_test(DefinedProcessTest(index, state.student_process, Feedback(_msg)))

    child = part_to_child(
        stu_part, sol_part, append_message, state, node_name="object_assignments"
    )

    return child


def is_instance(state, inst, not_instance_msg=None):
    """Check whether an object is an instance of a certain class.

    ``is_instance()`` can currently only be used when chained from ``check_object()``, the function that is
    used to 'zoom in' on the object of interest.

    Args:
        inst (class): The class that the object should have.
        not_instance_msg (str): When specified, this overrides the automatically generated message in case
            the object does not have the expected class.
        state (State): The state that is passed in through the SCT chain (don't specify this).

    :Example:

        Student code and solution code::

            import numpy as np
            arr = np.array([1, 2, 3, 4, 5])

        SCT::

            # Verify the class of arr
            import numpy
            Ex().check_object('arr').is_instance(numpy.ndarray)
    """

    state.assert_is(["object_assignments"], "is_instance", ["check_object"])

    sol_name = state.solution_parts.get("name")
    stu_name = state.student_parts.get("name")

    if not_instance_msg is None:
        not_instance_msg = "Is it a {{inst.__name__}}?"

    if not isInstanceInProcess(sol_name, inst, state.solution_process):
        raise InstructorError(
            "`is_instance()` noticed that `%s` is not a `%s` in the solution process."
            % (sol_name, inst.__name__)
        )

    _msg = state.build_message(not_instance_msg, {"inst": inst})
    feedback = Feedback(_msg, state)
    state.do_test(InstanceProcessTest(stu_name, inst, state.student_process, feedback))

    return state


def check_df(state, index, missing_msg=None, not_instance_msg=None, expand_msg=None):
    """Check whether a DataFrame was defined and it is the right type

    ``check_df()`` is a combo of ``check_object()`` and ``is_instance()`` that checks whether the specified object exists
    and whether the specified object is pandas DataFrame.

    You can continue checking the data frame with ``check_keys()`` function to 'zoom in' on a particular column in the pandas DataFrame:

    Args:
        index (str): Name of the data frame to zoom in on.
        missing_msg (str): See ``check_object()``.
        not_instance_msg (str): See ``is_instance()``.
        expand_msg (str): If specified, this overrides any messages that are prepended by previous SCT chains.

    :Example:

        Suppose you want the student to create a DataFrame ``my_df`` with two columns.
        The column ``a`` should contain the numbers 1 to 3,
        while the contents of column ``b`` can be anything: ::

            import pandas as pd
            my_df = pd.DataFrame({"a": [1, 2, 3], "b": ["a", "n", "y"]})

        The following SCT would robustly check that: ::

            Ex().check_df("my_df").multi(
                check_keys("a").has_equal_value(),
                check_keys("b")
            )

        - ``check_df()`` checks if ``my_df`` exists (``check_object()`` behind the scenes) and is a DataFrame (``is_instance()``)
        - ``check_keys("a")`` zooms in on the column ``a`` of the data frame, and ``has_equal_value()`` checks if the columns correspond between student and solution process.
        - ``check_keys("b")`` zooms in on hte column ``b`` of the data frame, but there's no 'equality checking' happening

        The following submissions would pass the SCT above: ::

            my_df = pd.DataFrame({"a": [1, 1 + 1, 3], "b": ["a", "l", "l"]})
            my_df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [7, 8, 9]})

    """
    child = check_object(
        state,
        index,
        missing_msg=missing_msg,
        expand_msg=expand_msg,
        typestr="pandas DataFrame",
    )
    is_instance(child, pd.DataFrame, not_instance_msg=not_instance_msg)
    return child


def check_keys(state, key, missing_msg=None, expand_msg=None):
    """Check whether an object (dict, DataFrame, etc) has a key.

    ``check_keys()`` can currently only be used when chained from ``check_object()``, the function that is
    used to 'zoom in' on the object of interest.

    Args:
        key (str): Name of the key that the object should have.
        missing_msg (str): When specified, this overrides the automatically generated
            message in case the key does not exist.
        expand_msg (str): If specified, this overrides any messages that are prepended by previous SCT chains.
        state (State): The state that is passed in through the SCT chain (don't specify this).

    :Example:

        Student code and solution code::

            x = {'a': 2}

        SCT::

            # Verify that x contains a key a
            Ex().check_object('x').check_keys('a')

            # Verify that x contains a key a and a is correct.
            Ex().check_object('x').check_keys('a').has_equal_value()

    """

    state.assert_is(["object_assignments"], "is_instance", ["check_object", "check_df"])

    if missing_msg is None:
        missing_msg = "There is no {{ 'column' if 'DataFrame' in parent.typestr else 'key' }} `'{{key}}'`."
    if expand_msg is None:
        expand_msg = "Did you correctly set the {{ 'column' if 'DataFrame' in parent.typestr else 'key' }} `'{{key}}'`? "

    sol_name = state.solution_parts.get("name")
    stu_name = state.student_parts.get("name")

    if not isDefinedCollInProcess(sol_name, key, state.solution_process):
        raise InstructorError(
            "`check_keys()` couldn't find key `%s` in object `%s` in the solution process."
            % (key, sol_name)
        )

    # check if key available
    _msg = state.build_message(missing_msg, {"key": key})
    state.do_test(
        DefinedCollProcessTest(
            stu_name, key, state.student_process, Feedback(_msg, state)
        )
    )

    def get_part(name, key, highlight):
        if isinstance(key, str):
            slice_val = ast.Str(s=key)
        else:
            slice_val = ast.parse(str(key)).body[0].value
        expr = ast.Subscript(
            value=ast.Name(id=name, ctx=ast.Load()),
            slice=ast.Index(value=slice_val),
            ctx=ast.Load(),
        )
        ast.fix_missing_locations(expr)
        return {"node": expr, "highlight": highlight}

    stu_part = get_part(stu_name, key, state.student_parts.get("highlight"))
    sol_part = get_part(sol_name, key, state.solution_parts.get("highlight"))
    append_message = {"msg": expand_msg, "kwargs": {"key": key}}
    child = part_to_child(stu_part, sol_part, append_message, state)
    return child
