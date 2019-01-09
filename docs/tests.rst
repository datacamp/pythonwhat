Tests
=====

.. note::

    The examples are numbered and linkable,
    but numbers (and links) can change between builds of the documentation.

.. jinja:: test_ctx

    {% for file, tests in test_data.items() %}

    {{ file }}
    {{ "-" * 100 }}

    {% for test in tests %}

    Example {{loop.index}}
    ~~~~~~~~~~~~~~~~~~~~~~
    {% if test.pre_exercise_code %}
    PEC ::

        {{ test.pre_exercise_code | indent(4) }}

    {% else %}
    No PEC
    {% endif %}
    {% if test.solution_code %}
    Solution code ::

        {{ test.solution_code | indent(4) }}

    {% else %}
    No solution code
    {% endif %}
    {% if test.student_code %}
    Student code ::

        {{ test.student_code | indent(4) }}

    {% else %}
    No student code
    {% endif %}
    {% if test.raw_student_output %}
    Student output ::

        {{ test.raw_student_output | indent(4) }}

    {% else %}
    No output
    {% endif %}
    {% if test.sct %}
    SCT ::

        {{ test.sct | indent(4) }}

    {% else %}
    No SCT
    {% endif %}
    {% if test.result %}
    Result ::

        {{ test.result.message | indent(4) }}

    {% else %}
    No result
    {% endif %}
    {% if test.error %}
    Error ::

        {{ test.error | indent(4) }}

    {% else %}
    No error
    {% endif %}

    {% endfor %}

    {% endfor %}
