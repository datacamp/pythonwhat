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
    """Test whether the student correctly coded a `try-except` block.  

    This function allows you to test specific parts of a try-except block.
    A try-except block consists of 4 parts: a body, error handlers, plus (rarely) an
    else and final block. ::

        try:              print(hello)
        except NameError: print('hello what?')
        except:           print('unexplained error')
        else:             print('else block')
        finally:          print('final block')
    
    Args:
        index (int): index of the try-except block to check. 
        not_called_msg: override the default message when too few try-except blocks found in student code.
        body: sub-sct to test the code of the `try` block. 
        handlers: a dictionary, where the keys are the error classes you expect the student to capture (for the general `except:`, use `'all'`), and the values are sub-SCTs for each of these `except` blocks.
        except_missing_message: override the default message when a expect block in the handlers arg is missing.
        orelse: similar to body, but for the else block.
        finalbody: similar to body, but for the finally block. 
        _missing_msg: custom messages if the orelse, or finalbody pieces are missing.
"""

    rep = Reporter.active_reporter

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
