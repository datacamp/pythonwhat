import ast
import inspect
from copy import copy
from pythonwhat.parsing import FunctionParser, ObjectAccessParser, parser_dict
from pythonwhat.Reporter import Reporter
from pythonwhat.Feedback import Feedback
from pythonwhat import utils_ast
from pythonwhat import signatures
from pythonwhat.converters import get_manual_converters

class State(object):
    """State of the SCT environment.

    This class holds all information relevevant to test the correctness of an exercise.
    It is coded suboptimally and it will be refactored soon, and documented thouroughly
    after that.

    """
    active_state = None
    converters = get_manual_converters()

    def __init__(self, student_parts=None, solution_parts=None, messages=None, **kwargs):

        # Set basic fields from kwargs
        self.__dict__.update(kwargs)

        self.student_parts = student_parts
        self.solution_parts = solution_parts
        self.messages = messages if messages else []

        # parse code if didn't happen yet
        if not hasattr(self, 'student_tree'):
            self.student_tree = State.parse_ext(self.student_code)

        if not hasattr(self, 'solution_tree'):
            self.solution_tree = State.parse_int(self.solution_code)

        if not hasattr(self, 'pre_exercise_tree'):
            self.pre_exercise_tree = State.parse_int(self.pre_exercise_code)

        if not hasattr(self, 'parent_state'):
            self.parent_state = None

        if not hasattr(self, 'student_context'):
            self.student_context = []

        if not hasattr(self, 'solution_context'):
            self.solution_context = []

        self.converters = None

        self.fun_usage = {}
        self.manual_sigs = None
        self._parser_cache = {}

    def get_converters(self):
        if self.converters is None:
            self.converters = get_manual_converters()

        return(self.converters)

    def set_used(self, name, stud_index, sol_index):
        if name in self.fun_usage.keys():
            self.fun_usage[name][sol_index] = stud_index
        else:
            self.fun_usage[name] = {sol_index: stud_index}

    def get_options(self, name, stud_indices, sol_index):
        if name in self.fun_usage.keys():
            if sol_index in self.fun_usage[name].keys():
                # sol_index has already been used
                return [self.fun_usage[name][sol_index]]
            else:
                # sol_index hasn't been used yet
                # exclude stud_index that have been hit elsewhere
                used = set(list(self.fun_usage[name].values()))
                return list(set(stud_indices) - used)
        else:
            return stud_indices

    def get_manual_sigs(self):
        if self.manual_sigs is None:
            self.manual_sigs = signatures.get_manual_sigs()

        return(self.manual_sigs)

    def build_message(self, tail="", fmt_kwargs=None):
        if not fmt_kwargs: fmt_kwargs = {}
        out_list = []
        # add trailing message to msg list
        msgs = self.messages[:] + [{'msg': tail or "", 'kwargs':fmt_kwargs}]
        # format messages in list, by iterating over previous, current, and next message
        for prev_d, d, next_d in zip([{}, *msgs[:-1]], msgs, [*msgs[1:], {}]):
            out = d['msg'].format(parent = prev_d.get('kwargs'),
                                  child = next_d.get('kwargs'),
                                  this = d['kwargs'],
                                  **d['kwargs'])
            out_list.append(out)

        return "".join(out_list)

    def update_message_keys(self, **kwargs):
        self.messages[-1]['kwargs'].update(kwargs)

    def to_child_state(self, student_subtree, solution_subtree, 
                             student_context=None, solution_context=None,
                             student_parts=None, solution_parts=None,
                             append_message=""):
        """Dive into nested tree.

        Set the current state as a state with a subtree of this syntax tree as
        student tree and solution tree. This is necessary when testing if statements or
        for loops for example.
        """

        if isinstance(student_subtree, list):
            student_subtree = ast.Module(student_subtree)
        if isinstance(solution_subtree, list):
            solution_subtree = ast.Module(solution_subtree)

        if student_context is None: student_context = self.student_context.copy()
        if solution_context is None: solution_context = self.solution_context.copy()
        if not isinstance(append_message, dict): 
            append_message =  {'msg': append_message, 'kwargs': {}}

        messages = [*self.messages, append_message]

        if not (solution_subtree and student_subtree):
            child = copy(self)
            child.student_context = student_context
            child.solution_context = solution_context
            child.solution_parts = solution_parts
            child.student_parts = student_parts
            child.messages = messages
            return child

        child = State(student_code = utils_ast.extract_text_from_node(self.full_student_code, student_subtree),
                      full_student_code = self.full_student_code,
                      pre_exercise_code = self.pre_exercise_code,
                      student_context = student_context,
                      solution_context  = solution_context,
                      student_process = self.student_process,
                      solution_process = self.solution_process,
                      raw_student_output = self.raw_student_output,
                      pre_exercise_tree = self.pre_exercise_tree,
                      student_tree = student_subtree,
                      solution_tree = solution_subtree,
                      student_parts = student_parts,
                      solution_parts = solution_parts,
                      messages = messages,
                      parent_state = self)
        State.set_active_state(child)
        return(child)

    def to_parent_state(self):
        if (self.parent_state):
            State.set_active_state(self.parent_state)


    @staticmethod
    def parse_ext(x):
        rep = Reporter.active_reporter

        res = None
        try:
            res = ast.parse(x)
            # enrich tree with end lines and end columns
            utils_ast.mark_text_ranges(res, x + '\n')

        except IndentationError as e:
            rep.set_tag("fun", "indentation_error")
            e.filename = "script.py"
            # no line info for now
            rep.feedback = Feedback("Your code could not be parsed due to an error in the indentation:<br>`%s.`" % str(e))
            rep.failed_test = True

        except SyntaxError as e:
            rep.set_tag("fun", "syntax_error")
            e.filename = "script.py"
            # no line info for now
            rep.feedback = Feedback("Your code can not be executed due to a syntax error:<br>`%s.`" % str(e))
            rep.failed_test = True

        # Can happen, can't catch this earlier because we can't differentiate between
        # TypeError in parsing or TypeError within code (at runtime).
        except:
            rep.set_tag("fun", "other_error")
            rep.feedback.message = "Something went wrong while parsing your code."
            rep.failed_test = True

        finally:
            if (res is None):
                res = False

        return(res)

    @staticmethod
    def parse_int(x):
        res = None
        try:
            res = ast.parse(x)
            utils_ast.mark_text_ranges(res, x + '\n')

        except SyntaxError as e:
            raise SyntaxError(str(e))
        except TypeError as e:
            raise TypeError(str(e))
        finally:
            if (res is None):
                res = False

        return(res)

    @staticmethod
    def set_active_state(state):
        State.active_state = state

# add property methods for retrieving parser outputs --------------------------
# note that this code is an alternative means of using something like..
#   @property
#   def student_withs(self): ...
# when defining the State class.
from functools import partial

def getx(tree_name, Parser, ext_attr, self): 
    """getter for Parser outputs"""
    # return cached output if possible
    cache_key = tree_name + Parser.__name__
    if self._parser_cache.get(cache_key):
        p = self._parser_cache[cache_key]
    else:
        # otherwise, run parser over tree
        p = Parser()
        p.visit(getattr(self, tree_name))
        # cache
        self._parser_cache[cache_key] = p
    return getattr(p, ext_attr)

def get_func_map(tree_name, ext_attr, self):
    """getter for FunctionParser outputs, uses pre_exercise_mappings"""
    cache_key = tree_name + FunctionParser.__name__
    if self._parser_cache.get(cache_key):
        p = self._parser_cache[cache_key]
    else:
        p = FunctionParser()
        p.mappings = self.pre_exercise_mappings.copy()
        p.visit(getattr(self, tree_name))
        self._parser_cache[cache_key] = p
    return getattr(p, ext_attr)
    
# put a property getter on state for each parsed ast tree output.
# since the getter takes only one argument, self, partial functions
# are used to set all other arguments on getx and get_func_map
for s in ['student', 'solution']:
    tree_name = s+'_tree'
    for k, Parser in parser_dict.items():
        setattr(State, s+'_'+k, property(partial(getx, tree_name, Parser, 'out')))

    # mappings from ObjectAccessParser
    prop_oa_map = property(partial(getx, tree_name, ObjectAccessParser, 'mappings'))
    setattr(State, s+'_oa_mappings', prop_oa_map)

    # Getters for FunctionParser -----
    # calls
    prop_calls = property(partial(get_func_map, tree_name, 'calls'))
    setattr(State, s+'_function_calls', prop_calls)
    # mappings
    prop_map = property(partial(get_func_map, tree_name, 'mappings'))
    setattr(State, s+'_mappings', prop_map)

pec_prop_map = property(partial(getx, 'pre_exercise_tree', FunctionParser, 'mappings'))
setattr(State, 'pre_exercise_mappings', pec_prop_map)


# global setters on State -----------------------------------------------------
def set_converter(key, fundef):
    State.converters[key] = fundef
