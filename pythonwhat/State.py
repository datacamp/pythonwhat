import ast
import inspect
import string
from copy import copy
from functools import partial
from pythonwhat.parsing import TargetVars, FunctionParser, ObjectAccessParser, parser_dict
from pythonwhat.Reporter import Reporter
from pythonwhat.Feedback import Feedback, InstructorError
from pythonwhat.Test import Test
from pythonwhat import signatures
from pythonwhat.converters import get_manual_converters
from collections.abc import Mapping
from itertools import chain
from jinja2 import Template
import asttokens
from pythonwhat.utils_ast import wrap_in_module

class Context(Mapping):
    def __init__(self, context=None, prev=None):
        self.context = context if context else TargetVars()
        self.prev = prev if prev else {}

        self._items = {**self.prev, **self.context.defined_items()}

    def update_ctx(self, new_ctx):
        upd_prev = {**self.prev, **self.context.defined_items()}
        return self.__class__(new_ctx, upd_prev)

    def __getitem__(self, x):
        return self._items[x]

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

class State(object):
    """State of the SCT environment.

    This class holds all information relevevant to test the correctness of an exercise.
    It is coded suboptimally and it will be refactored soon, and documented thouroughly
    after that.

    """
    def __init__(self, 
                 student_context=None, solution_context=None,
                 student_env=None, solution_env=None,
                 student_parts=None, solution_parts=None, 
                 highlight = None,
                 highlighting_disabled = None, messages=None,
                 **kwargs):

        # Set basic fields from kwargs
        self.__dict__.update(kwargs)

        self.student_parts = student_parts
        self.solution_parts = solution_parts
        self.messages = messages if messages else []

        # parse code if didn't happen yet
        if not hasattr(self, 'student_tree'):
            self.student_tree_tokens, self.student_tree = State.parse_external(self.student_code)

        if not hasattr(self, 'solution_tree'):
            self.solution_tree_tokens, self.solution_tree = State.parse_internal(self.solution_code)

        if not hasattr(self, 'pre_exercise_tree'):
            _, self.pre_exercise_tree = State.parse_internal(self.pre_exercise_code)

        if not hasattr(self, 'parent_state'):
            self.parent_state = None

        self.student_context  = Context(student_context)  if student_context is None else student_context
        self.solution_context = Context(solution_context) if solution_context is None else solution_context
        self.student_env = Context(student_env) if student_env is None else student_env
        self.solution_env = Context(solution_env) if solution_env is None else solution_env

        self.highlight = self.student_tree if (not highlight) and self.parent_state else highlight
        self.highlighting_disabled = highlighting_disabled

        self.converters = get_manual_converters()    # accessed only from root state

        self.manual_sigs = None
        self._parser_cache = {}

    def get_manual_sigs(self):
        if self.manual_sigs is None:
            self.manual_sigs = signatures.get_manual_sigs()

        return(self.manual_sigs)

    def build_message(self, tail="", fmt_kwargs=None, append=True):

        if not fmt_kwargs: fmt_kwargs = {}
        out_list = []
        # add trailing message to msg list
        msgs = self.messages[:] + [{'msg': tail or "", 'kwargs':fmt_kwargs}]
        # format messages in list, by iterating over previous, current, and next message
        for prev_d, d, next_d in zip([{}, *msgs[:-1]], msgs, [*msgs[1:], {}]):
            tmp_kwargs = {'parent': prev_d.get('kwargs'), 
                          'child': next_d.get('kwargs'), 
                          'this': d['kwargs'], 
                          **d['kwargs']}
            # don't bother appending if there is no message
            if not d['msg']:
                continue
            out = Template(d['msg'].replace('__JINJA__:', "")).render(**tmp_kwargs)
            out_list.append(out)

        # if highlighting info is available, don't put all expand messages
        if self.highlight and not self.highlighting_disabled:
            out_list = out_list[-3:]

        if append:
            return "".join(out_list)
        else:
            return out_list[-1]

    def to_child_state(self, student_subtree=None, solution_subtree=None,
                             student_context=None, solution_context=None,
                             student_env=None, solution_env=None,
                             student_parts=None, solution_parts=None,
                             highlight = None,
                             highlighting_disabled = None,
                             append_message="", node_name=""):
        """Dive into nested tree.

        Set the current state as a state with a subtree of this syntax tree as
        student tree and solution tree. This is necessary when testing if statements or
        for loops for example.
        """

        if isinstance(student_subtree, list):
            student_subtree = wrap_in_module(student_subtree)
        if isinstance(solution_subtree, list):
            solution_subtree = wrap_in_module(solution_subtree)

        # get new contexts
        if solution_context is not None: 
            solution_context = self.solution_context.update_ctx(solution_context)
        else:
            solution_context = self.solution_context

        if student_context is not None:
            student_context = self.student_context.update_ctx(student_context)
        else:
            student_context = self.student_context

        # get new envs
        if solution_env is not None:
            solution_env = self.solution_env.update_ctx(solution_env)
        else:
            solution_env = self.solution_env

        if student_env is not None:
            student_env = self.student_env.update_ctx(student_env)
        else:
            student_env = self.student_env

        if highlighting_disabled is None:
            highlighting_disabled = self.highlighting_disabled

        if not isinstance(append_message, dict): 
            append_message =  {'msg': append_message, 'kwargs': {}}

        messages = [*self.messages, append_message]

        if not (solution_subtree and student_subtree):
            return self.update(student_context = student_context, solution_context = solution_context,
                               student_env = student_env, solution_env = solution_env,
                               highlight = highlight,
                               highlighting_disabled = highlighting_disabled,
                               messages = messages)

        klass = State if not node_name else self.SUBCLASSES[node_name]
        child = klass(student_code = self.student_tree_tokens.get_text(student_subtree),
                      solution_code = self.solution_tree_tokens.get_text(solution_subtree),
                      student_tree_tokens = self.student_tree_tokens,
                      solution_tree_tokens = self.solution_tree_tokens,
                      pre_exercise_code = self.pre_exercise_code,
                      student_context = student_context,
                      solution_context  = solution_context,
                      student_env = student_env,
                      solution_env = solution_env,
                      student_process = self.student_process,
                      solution_process = self.solution_process,
                      raw_student_output = self.raw_student_output,
                      pre_exercise_tree = self.pre_exercise_tree,
                      student_tree = student_subtree,
                      solution_tree = solution_subtree,
                      student_parts = student_parts,
                      solution_parts = solution_parts,
                      highlight = highlight,
                      highlighting_disabled = highlighting_disabled,
                      messages = messages,
                      parent_state = self)
        return(child)

    def update(self, **kwargs):
        """Return a copy of set, setting kwargs as attributes"""
        child = copy(self)
        for k, v in kwargs.items():
            setattr(child, k, v)
        return child

    def has_different_processes(self):
        # process classes have an _identity field that is a tuple
        try:
            return self.student_process._identity[0] != self.solution_process._identity[0]
        except:
            # play it safe (most common)
            return True

    def assert_root(self, fun):
        if self.parent_state is not None:
            raise InstructorError("`%s()` should only be called from the root state, `Ex()`." % fun)

    def assert_is(self, klasses, fun, prev_fun):
        if self.__class__.__name__ not in klasses:
            raise InstructorError("`%s()` can only be called on %s." %
                (fun, " or ".join([ '`%s()`' % pf for pf in prev_fun ]))
            )

    def assert_is_not(self, klasses, fun, prev_fun):
        if self.__class__.__name__ in klasses:
            raise InstructorError("`%s()` should not be called on %s." %
                (fun, " or ".join([ '`%s()`' % pf for pf in prev_fun ]))
            )

    @staticmethod
    def parse_external(x):
        rep = Reporter.active_reporter

        res = (None, None)
        try:
            res = asttokens.ASTTokens(x, parse = True)
            return(res, res._tree)

        except IndentationError as e:
            e.filename = "script.py"
            # no line info for now
            rep.do_test(Test(Feedback("Your code could not be parsed due to an error in the indentation:<br>`%s.`" % str(e))))

        except SyntaxError as e:
            e.filename = "script.py"
            # no line info for now
            rep.do_test(Test(Feedback("Your code can not be executed due to a syntax error:<br>`%s.`" % str(e))))

        # Can happen, can't catch this earlier because we can't differentiate between
        # TypeError in parsing or TypeError within code (at runtime).
        except:
            rep.do_test(Test(Feedback("Something went wrong while parsing your code.")))

        return(res)

    @staticmethod
    def parse_internal(x):
        res = (None, None)
        try:
            res = asttokens.ASTTokens(x, parse = True)
            return(res, res._tree)
        except Exception as e:
            raise InstructorError("Something went wrong when parsing PEC or solution code: %s" % str(e))

# add property methods for retrieving parser outputs --------------------------
# note that this code is an alternative means of using something like..
#   @property
#   def student_withs(self): ...
# when defining the State class.
def getx(tree_name, Parser, ext_attr, self): 
    """getter for Parser outputs"""
    # return cached output if possible
    cache_key = tree_name + Parser.__name__
    if self._parser_cache.get(cache_key):
        p = self._parser_cache[cache_key]
    else:
        # otherwise, run parser over tree
        p = Parser()
        # set mappings for parsers that inspect attribute access
        if ext_attr != 'mappings' and Parser in [FunctionParser, ObjectAccessParser]: 
            p.mappings = self.pre_exercise_mappings.copy()
        # run parser
        p.visit(getattr(self, tree_name))
        # cache
        self._parser_cache[cache_key] = p
    return getattr(p, ext_attr)

# put a property getter on state for each parsed ast tree output.
# since the getter takes only one argument, self, partial functions
# are used to set all other arguments on getx
for s in ['student', 'solution']:
    tree_name = s+'_tree'
    for k, Parser in parser_dict.items():
        setattr(State, s+'_'+k, property(partial(getx, tree_name, Parser, 'out')))

    # mappings from ObjectAccessParser
    prop_oa_map = property(partial(getx, tree_name, ObjectAccessParser, 'mappings'))
    setattr(State, s+'_oa_mappings', prop_oa_map)

    # mappings from FunctionParser
    prop_map = property(partial(getx, tree_name, FunctionParser, 'mappings'))
    setattr(State, s+'_mappings', prop_map)

# mappings for pre exercise code from FunctionParser
pec_prop_map = property(partial(getx, 'pre_exercise_tree', FunctionParser, 'mappings'))
setattr(State, 'pre_exercise_mappings', pec_prop_map)

# State subclasses based on parsed output -------------------------------------
State.SUBCLASSES = {node_name: type(node_name, (State,), {}) for node_name in parser_dict}

# global setters on State -----------------------------------------------------
def set_converter(key, fundef):
    # note that root state is set on the State class in test_exercise
    State.root_state.converters[key] = fundef
