import ast
import inspect
from pythonwhat.parsing import FunctionParser, ObjectAccessParser, ObjectAssignmentParser, IfParser, WhileParser, ForParser, OperatorParser, ImportParser, FunctionDefParser, LambdaFunctionParser, ListCompParser, DictCompParser, GeneratorExpParser, WithParser, TryExceptParser
from pythonwhat.Reporter import Reporter
from pythonwhat.Feedback import Feedback
from pythonwhat import utils_ast
from pythonwhat import signatures

class State(object):
    """State of the SCT environment.

    This class holds all information relevevant to test the correctness of an exercise.
    It is coded suboptimally and it will be refactored soon, and documented thouroughly
    after that.

    """
    active_state = None

    def __init__(self, **kwargs):

        # Set basic fields from kwargs
        self.__dict__.update(kwargs)

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
            self.student_context = None

        if not hasattr(self, 'solution_context'):
            self.solution_context = None

        self.student_operators = None
        self.solution_operators = None

        self.pre_exercise_mappings = None
        self.student_function_calls = None
        self.solution_function_calls = None
        self.student_mappings = None
        self.solution_mappings = None
        self.fun_usage = None
        self.manual_sigs = None

        self.student_object_accesses = None
        self.student_object_assignments = None

        self.student_imports = None
        self.solution_imports = None

        self.student_if_calls = None
        self.solution_if_calls = None

        self.student_while_calls = None
        self.solution_while_calls = None

        self.student_for_calls = None
        self.solution_for_calls = None

        self.student_function_defs = None
        self.solution_function_defs = None

        self.student_lambda_functions = None
        self.solution_lambda_functions = None

        self.student_list_comps = None
        self.solution_list_comps = None

        self.student_dict_comps = None
        self.solution_dict_comps = None

        self.student_generator_exps = None
        self.solution_generator_exps = None

        self.student_withs = None
        self.solution_withs = None

        self.student_try_excepts = None
        self.solution_try_excepts = None


    def extract_operators(self):
        if (self.student_operators is None):
            op = OperatorParser()
            op.visit(self.student_tree)
            self.student_operators = op.ops

        if (self.solution_operators is None):
            op = OperatorParser()
            op.visit(self.solution_tree)
            self.solution_operators = op.ops

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

    def extract_function_calls(self):
        if (self.fun_usage is None):
            self.fun_usage = {}

        if (self.pre_exercise_mappings is None):
            fp = FunctionParser()
            fp.visit(self.pre_exercise_tree)
            self.pre_exercise_mappings = fp.mappings

        if (self.student_function_calls is None):
            fp = FunctionParser()
            fp.mappings = self.pre_exercise_mappings.copy()
            fp.visit(self.student_tree)
            self.student_function_calls = fp.calls
            self.student_mappings = fp.mappings

        if (self.solution_function_calls is None):
            fp = FunctionParser()
            fp.mappings = self.pre_exercise_mappings.copy()
            fp.visit(self.solution_tree)
            self.solution_function_calls = fp.calls
            self.solution_mappings = fp.mappings

    def get_manual_sigs(self):
        if self.manual_sigs is None:
            self.manual_sigs = signatures.get_manual_sigs()

        return(self.manual_sigs)

    def extract_object_accesses(self):
        if (self.student_object_accesses is None):
            oap = ObjectAccessParser()
            oap.visit(self.student_tree)
            self.student_object_accesses = oap.accesses
            self.student_mappings = oap.mappings

    def extract_object_assignments(self):
        if (self.student_object_assignments is None):
            oap = ObjectAssignmentParser()
            oap.visit(self.student_tree)
            self.student_object_assignments = oap.assignments

    def extract_imports(self):
        if (self.student_imports is None):
            ip = ImportParser()
            ip.visit(self.student_tree)
            self.student_imports = ip.imports

        if (self.solution_imports is None):
            ip = ImportParser()
            ip.visit(self.solution_tree)
            self.solution_imports = ip.imports

    def extract_if_calls(self):
        if (self.student_if_calls is None):
            ip = IfParser()
            ip.visit(self.student_tree)
            self.student_if_calls = ip.ifs

        if (self.solution_if_calls is None):
            ip = IfParser()
            ip.visit(self.solution_tree)
            self.solution_if_calls = ip.ifs

    def extract_while_calls(self):
        if (self.student_while_calls is None):
            ip = WhileParser()
            ip.visit(self.student_tree)
            self.student_while_calls = ip.whiles

        if (self.solution_while_calls is None):
            ip = WhileParser()
            ip.visit(self.solution_tree)
            self.solution_while_calls = ip.whiles

    def extract_for_calls(self):
        if (self.student_for_calls is None):
            fp = ForParser()
            fp.visit(self.student_tree)
            self.student_for_calls = fp.fors

        if (self.solution_for_calls is None):
            fp = ForParser()
            fp.visit(self.solution_tree)
            self.solution_for_calls = fp.fors

    def extract_function_defs(self):
        if (self.student_function_defs is None):
            fp = FunctionDefParser()
            fp.visit(self.student_tree)
            self.student_function_defs = fp.defs

        if (self.solution_function_defs is None):
            fp = FunctionDefParser()
            fp.visit(self.solution_tree)
            self.solution_function_defs = fp.defs

    def extract_lambda_functions(self):
        if (self.student_lambda_functions is None):
            lfp = LambdaFunctionParser()
            lfp.visit(self.student_tree)
            self.student_lambda_functions = lfp.funs

        if (self.solution_lambda_functions is None):
            lfp = LambdaFunctionParser()
            lfp.visit(self.solution_tree)
            self.solution_lambda_functions = lfp.funs

    def extract_list_comps(self):
        if self.student_list_comps is None:
            lcp = ListCompParser()
            lcp.visit(self.student_tree)
            self.student_list_comps = lcp.comps

        if self.solution_list_comps is None:
            lcp = ListCompParser()
            lcp.visit(self.solution_tree)
            self.solution_list_comps = lcp.comps

    def extract_dict_comps(self):
        if self.student_dict_comps is None:
            dcp = DictCompParser()
            dcp.visit(self.student_tree)
            self.student_dict_comps = dcp.comps

        if self.solution_dict_comps is None:
            dcp = DictCompParser()
            dcp.visit(self.solution_tree)
            self.solution_dict_comps = dcp.comps

    def extract_generator_exps(self):
        if self.student_generator_exps is None:
            gep = GeneratorExpParser()
            gep.visit(self.student_tree)
            self.student_generator_exps = gep.comps

        if self.solution_dict_comps is None:
            gep = GeneratorExpParser()
            gep.visit(self.solution_tree)
            self.solution_generator_exps = gep.comps

    def extract_withs(self):
        if (self.student_withs is None):
            wp = WithParser()
            wp.visit(self.student_tree)
            self.student_withs = wp.withs

        if (self.solution_withs is None):
            wp = WithParser()
            wp.visit(self.solution_tree)
            self.solution_withs = wp.withs

    def extract_try_excepts(self):
        if (self.student_try_excepts is None):
            tep = TryExceptParser()
            tep.visit(self.student_tree)
            self.student_try_excepts = tep.try_excepts

        if (self.solution_try_excepts is None):
            tep = TryExceptParser()
            tep.visit(self.solution_tree)
            self.solution_try_excepts = tep.try_excepts

    def to_child_state(self, student_subtree, solution_subtree):
        """Dive into nested tree.

        Set the current state as a state with a subtree of this syntax tree as
        student tree and solution tree. This is necessary when testing if statements or
        for loops for example.
        """

        if isinstance(student_subtree, list):
            student_subtree = ast.Module(student_subtree)
        if isinstance(solution_subtree, list):
            solution_subtree = ast.Module(solution_subtree)

        child = State(student_code = utils_ast.extract_text_from_node(self.full_student_code, student_subtree),
                      full_student_code = self.full_student_code,
                      pre_exercise_code = self.pre_exercise_code,
                      student_env = self.student_env,
                      solution_env = self.solution_env,
                      student_context = self.student_context,
                      solution_context  = self.solution_context,
                      raw_student_output = self.raw_student_output,
                      pre_exercise_tree = self.pre_exercise_tree,
                      student_tree = student_subtree,
                      solution_tree = solution_subtree,
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
