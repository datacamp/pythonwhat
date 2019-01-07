Tests
=====

{% for member in tests %}
Example {{loop.index}}
----------------------
{% if member.pre_exercise_code %}
PEC ::

    {{ member.pre_exercise_code | indent(4) }}

{% else %}
No PEC
{% endif %}
{% if member.solution_code %}
Solution code ::

    {{ member.solution_code | indent(4) }}

{% else %}
No solution code
{% endif %}
{% if member.student_code %}
Student code ::

    {{ member.student_code | indent(4) }}

{% else %}
No student code
{% endif %}
{% if member.raw_student_output %}
Student output ::

    {{ member.raw_student_output | indent(4) }}

{% else %}
No output
{% endif %}
{% if member.sct %}
SCT ::

    {{ member.sct | indent(4) }}

{% else %}
No SCT
{% endif %}
{% if member.result %}
Result ::

    {{ member.result.message | indent(4) }}

{% else %}
No result
{% endif %}
{% if member.error %}
Error ::

    {{ member.error | indent(4) }}

{% else %}
No error
{% endif %}

{% endfor %}
