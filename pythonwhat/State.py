import ast
import inspect
from pythonwhat.parsing import FunctionParser, IfParser, WhileParser, ForParser, OperatorParser, ImportParser, FunctionDefParser, FindLastLineParser, WithParser

from pythonwhat.Reporter import Reporter

# TODO (Vincent): refactor using dict: e.g. parsed_solution['functions'] => FunctionParser()
class State(object):
    """State of the SCT environment.

    This class holds all information relevevant to test the correctness of an exercise.
    It is coded suboptimally and it will be refactored soon, and documented thouroughly
    after that.

    """
    active_state = None

    def __init__(
            self,
            student_code,
            solution_code,
            pre_exercise_code,
            student_env,
            solution_env,
            raw_student_output):
        self.add_student_code(student_code)
        self.add_solution_code(solution_code)
        self.add_pre_exercise_code(pre_exercise_code)
        self.add_student_env(student_env)
        self.add_solution_env(solution_env)
        self.add_raw_student_output(raw_student_output)

        self.student_tree = None
        self.solution_tree = None
        self.pre_exercise_tree = None

        self.student_operators = None
        self.solution_operators = None

        self.pre_exercise_imports = None
        self.student_function_calls = None
        self.solution_function_calls = None
        self.used_student_function = None

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

        self.student_withs = None
        self.solution_withs = None

        self.parent_state = None

    def add_student_code(self, student_code):
        assert isinstance(
            student_code, str), "student_code is not a string: %r" % student_code
        self.student_code = student_code

    def add_solution_code(self, solution_code):
        assert isinstance(
            solution_code, str), "solution_code is not a string: %r" % solution_code
        self.solution_code = solution_code

    def add_pre_exercise_code(self, pre_exercise_code):
        assert isinstance(
            pre_exercise_code, str), "pre_exercise_code is not a string: %r" % pre_exercise_code
        self.pre_exercise_code = pre_exercise_code

    def add_student_env(self, student_env):
        assert isinstance(
            student_env, dict), "student_env is not a dictionary: %r" % student_env
        self.student_env = student_env

    def add_solution_env(self, solution_env):
        assert isinstance(
            solution_env, dict), "solution_env is not a dictionary: %r" % solution_env
        self.solution_env = solution_env

    def add_raw_student_output(self, raw_student_output):
        assert isinstance(
            raw_student_output, str), "raw_student_output is not a string: %r" % raw_student_output
        self.raw_student_output = raw_student_output

    def parse_code(self):
        if (self.student_tree is None):
            rep = Reporter.active_reporter

            try:
                self.student_tree = ast.parse(self.student_code)
            # Should never happen, SyntaxErrors are handled sooner.
            except IndentationError as e:
                rep.fail(
                    "Your code can not be executed due to an error in the indentation: %s." %
                    str(e))
            except SyntaxError as e:
                rep.fail(
                    "Your code can not be executed due to a syntax error: %s." %
                    str(e))

            # Can happen, can't catch this earlier because we can't differentiate between
            # TypeError in parsing or TypeError within code (at runtime).
            except TypeError as e:
                rep.fail("Something went wrong while running your code.")
            finally:
                if (self.student_tree is None):
                    self.student_tree = False

        if (self.solution_tree is None):
            try:
                self.solution_tree = ast.parse(self.solution_code)
            except SyntaxError as e:
                raise SyntaxError("In solution code: " + str(e))
            except TypeError as e:
                raise TypeError("In solution code: " + str(e))
            finally:
                if (self.solution_tree is None):
                    self.solution_tree = False

        if (self.pre_exercise_tree is None):
            try:
                self.pre_exercise_tree = ast.parse(self.pre_exercise_code)
            except SyntaxError as e:
                raise SyntaxError("In pre exercise code: " + str(e))
            except TypeError as e:
                raise TypeError("In pre exercise code: " + str(e))
            finally:
                if (self.pre_exercise_tree is None):
                    self.pre_exercise_tree = False

    def extract_operators(self):
        self.parse_code()

        if (self.student_operators is None):
            op = OperatorParser()
            op.visit(self.student_tree)
            self.student_operators = op.ops

        if (self.solution_operators is None):
            op = OperatorParser()
            op.visit(self.solution_tree)
            self.solution_operators = op.ops

    def extract_function_calls(self):
        self.parse_code()

        if (self.used_student_function is None):
            self.used_student_function = {}

        if (self.pre_exercise_imports is None):
            fp = FunctionParser()
            fp.visit(self.pre_exercise_tree)
            self.pre_exercise_imports = fp.imports

        if (self.student_function_calls is None):
            fp = FunctionParser()
            fp.imports = self.pre_exercise_imports
            fp.visit(self.student_tree)
            self.student_function_calls = fp.calls

        if (self.solution_function_calls is None):
            fp = FunctionParser()
            fp.imports = self.pre_exercise_imports
            fp.visit(self.solution_tree)
            self.solution_function_calls = fp.calls

    def extract_imports(self):
        self.parse_code()

        if (self.student_imports is None):
            ip = ImportParser()
            ip.visit(self.student_tree)
            self.student_imports = ip.imports

        if (self.solution_imports is None):
            ip = ImportParser()
            ip.visit(self.solution_tree)
            self.solution_imports = ip.imports

    def extract_if_calls(self):
        self.parse_code()

        if (self.student_if_calls is None):
            ip = IfParser()
            ip.visit(self.student_tree)
            self.student_if_calls = ip.ifs

        if (self.solution_if_calls is None):
            ip = IfParser()
            ip.visit(self.solution_tree)
            self.solution_if_calls = ip.ifs

    def extract_while_calls(self):
        self.parse_code()

        if (self.student_while_calls is None):
            ip = WhileParser()
            ip.visit(self.student_tree)
            self.student_while_calls = ip.whiles

        if (self.solution_while_calls is None):
            ip = WhileParser()
            ip.visit(self.solution_tree)
            self.solution_while_calls = ip.whiles

    def extract_for_calls(self):
        self.parse_code()

        if (self.student_for_calls is None):
            fp = ForParser()
            fp.visit(self.student_tree)
            self.student_for_calls = fp.fors

        if (self.solution_for_calls is None):
            fp = ForParser()
            fp.visit(self.solution_tree)
            self.solution_for_calls = fp.fors

    def extract_function_defs(self):
        self.parse_code()

        if (self.student_function_defs is None):
            fp = FunctionDefParser()
            fp.visit(self.student_tree)
            self.student_function_defs = fp.defs

        if (self.solution_function_defs is None):
            fp = FunctionDefParser()
            fp.visit(self.solution_tree)
            self.solution_function_defs = fp.defs

    def extract_withs(self):
        self.parse_code()

        if (self.student_withs is None):
            wp = WithParser()
            wp.visit(self.student_tree)
            self.student_withs = wp.withs

        if (self.solution_withs is None):
            wp = WithParser()
            wp.visit(self.solution_tree)
            self.solution_withs = wp.withs

    def extract_object_accesses(self):
        self.parse_code()

        if (self.student_object_accesses is None):
            oap = ObjectAccessParser()
            oap.visit(self.student_tree)
            self.student_object_accesses = oap.object_accesses

        if (self.solution_object_accesses is None):
            oap = ObjectAccessParser()
            oap.visit(self.solution_tree)
            self.solution_object_accesses = oap.object_accesses

    def to_child_state(self, student_subtree, solution_subtree):
        """Dive into nested tree.

        Set the current state as a state with a subtree of this syntax tree as
        student tree and solution tree. This is necessary when testing if statements or
        for loops for example.
        """

        args = inspect.signature(self.__class__.__init__)
        arg_values = [self.__dict__[arg] for arg in list(args.parameters.keys())[1:]]
        child = State(*arg_values)
        child.student_tree = student_subtree
        child.solution_tree = solution_subtree
        child.student_code = State.get_subcode(
            student_subtree, self.student_code)
        child.solution_code = State.get_subcode(
            solution_subtree, self.solution_code)
        child.parent_state = self
        State.set_active_state(child)
        return(child)

    def get_subcode(subtree, full_code):
        """Extract code subtree.

        Extract all the code belonging to a subtree of the code.
        """
        try:
            if isinstance(subtree, list):
                subtree = ast.Module(body=subtree)

            begin = subtree.body[0].lineno - 1
            ll = FindLastLineParser()
            ll.visit(subtree)
            end = ll.last_line

            return("\n".join(full_code.split("\n")[begin:end]))
        except:
            return ""

    def to_parent_state(self):
        if (self.parent_state):
            State.set_active_state(self.parent_state)

    def set_active_state(to_state):
        State.active_state = to_state
