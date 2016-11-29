from pythonwhat.Reporter import Reporter
from pythonwhat.check_funcs import check_node, check_part, check_part_index, multi, quiet
from functools import partial

MSG_MISSING = "FMT:The system wants to check the {ordinal} try-except block you defined but hasn't found it."
MSG_PREPEND = "FMT:Check your code in the {child[part]} of the {ordinal} {typestr}. "
MSG_MISSING_PART  = "FMT:Have you included a {part} in your {parent[ordinal]} {parent[typestr]}?"

def test_try_except(index=1,
                    not_called_msg=None,
                    body=None,
                    handlers={},
                    except_missing_msg = None,
                    orelse=None,
                    orelse_missing_msg=None,
                    finalbody=None,
                    finalbody_missing_msg=None,
                    expand_message=True,
                    state=None):
    """Test a try except construct
    """

    rep = Reporter.active_reporter
    rep.set_tag("fun", "test_try_except")

    # TODO: alternatively, could have missing_msg not use prepended messages
    #       then we wouldn't have to run check_part twice for everything
    child = check_node('try_excepts', index-1, "try-except block", MSG_MISSING, MSG_PREPEND, state)
    quiet_child = quiet(1, state=child)

    multi(body, state=check_part("body", "body", child))       # subtests

    # handler tests
    for key,value in handlers.items():
        incorrect_part = "{} `except` block".format('general' if key == 'all' else "`%s`"%key)

        # run to see if index exists, since the message depends on using the quiet child :o
        check_handler = partial(check_part_index, 'handlers', key, incorrect_part, MSG_MISSING_PART)

        check_handler(state=quiet_child)                       # exists
        multi(value, state=check_handler(state=child))         # subtests

    # test orelse and finalbody
    check = partial(check_part, missing_msg = MSG_MISSING_PART)

    # test orelse 
    if child.solution_parts['orelse']:
        check('orelse', "`else` part", quiet_child)                         # exists
        multi(orelse, state=check('orelse', "`else` part", child))          # subtests

    # test orelse 
    if child.solution_parts['finalbody']:
        check('finalbody', "`finally` part", quiet_child)                   # exists
        multi(finalbody, state=check('finalbody', "`finally` part", child)) # subtests
