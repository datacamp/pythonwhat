import ast

"""
This file handles the parsing of the student and solution code. Generally, an abstract syntax tree
is built from the code string and this tree is passed to several visitors to create the data
structures that are used by the tests.

For information about how the ast package works, I refer to its documentation:
    https://docs.python.org/2/library/ast.html
as well as some extra documentation:
    https://greentreesnakes.readthedocs.org/en/latest/
"""


class Parser(ast.NodeVisitor):
    """Basic parser.

    The basic Parser, should not be used directly, but to inherit from. The Parser itself inherits
    from ast.Nodevisitor, which is a helper class to go through the abstract syntax tree objects.

    In the basic version, each node in the Module body will be visited. Expression bodies will be
    visited as well. In this standard parser, all other nodes are ignored.
    """

    def visit_Module(self, node):
        """
        This function is called when a Module node is encountered when traversing the tree.

        Args:
            node (ast.Module): The node which is visited.
        """
        for line in node.body:
            # We only want to visit the module nodes on a first level. Going deeper
            # should be handeled by the specific parsers and the test function, as
            # nesting requires the State to generate a subtree. The Parser object
            # does not know about the State object.
            self.visit(line)

    def visit_Expr(self, node):
        self.visit(node.value)

    def visit_Expression(self, node):
        self.visit(node.body)

    def generic_visit(self, node):
        """
        This function is called when all other nodes are encountered when traversing the tree.
        When inheriting form this standard parser, this function will make the parser ignore
        all nodes that are not relevant.

        Args:
            node (ast.Node): The node which is visited.
        """
        pass  # This ignore is necessary to keep the parser at base level, also look comment above in
              # the visit_Module function body.

    def visit_each(self, lst):
        for el in lst:
            self.visit(el)

    @staticmethod
    def get_target_vars(target):
        if isinstance(target, ast.Name):
            return [target.id]
        elif isinstance(target, ast.Tuple):
            return [name.id for name in target.elts]
        else:
            return []

class OperatorParser(Parser):
    """Find operations.

    A parser which inherits from the basic parser to find binary operators.

    Attributes:
        ops (list(tuple(num, ast.BinOp, list(str)))): A list of tuples containing the linenumber, node and list of used binary operations.
        level (num): A number representing the level at which the parser is parsing.
        used (list(str)): The operators that are used in the BinOp that we're handling.
    """


    # All possible operations and their sign
    O_MAP = {}
    O_MAP['Add'] = '+'
    O_MAP['Sub'] = '-'
    O_MAP['Mult'] = '*'
    O_MAP['Div'] = '/'
    O_MAP['Mod'] = '%'
    O_MAP['Pow'] = '**'
    O_MAP['LShift'] = '<<'
    O_MAP['RShift'] = '>>'
    O_MAP['BitOr'] = '|'
    O_MAP['BitXor'] = '^'
    O_MAP['BitAnd'] = '&'
    O_MAP['FloorDiv'] = '//'

    def __init__(self):
        """
        Initialize the parser and its attributes.
        """
        self.ops = []
        self.level = 0
        self.used = []

    def visit_Expr(self, node):
        self.visit(node.value)

    def visit_Call(self, node):
        for arg in node.args:
            self.visit(arg)

    def visit_Assign(self, node):
        self.visit(node.value)

    def visit_Num(self, node):
        if not self.level:
            self.ops.append((  # A number can be seen as a operator on base level.
                node,          # When student is asked to use operators but just puts in a number instead,
                self.used))    # this will help creating a consistent feedback message.

    def visit_UnaryOp(self, node):
        self.visit(node.operand)  # Unary operations, like '-', should not be added, but they should be
        # looked into. They can contain more binary operations. This is important
        # during the nesting process.

    def visit_BinOp(self, node):
        self.used.append(OperatorParser.O_MAP[type(node.op).__name__])
        self.level = self.level + 1
        # Nest to other operations, but increase the level. We only
        self.visit(node.left)
        # want to now which operations are used at a deeper level, but
        self.visit(node.right)
        self.level = self.level - 1  # we don't need all the explicit nodes.

        if not self.level:          # We should only add the binary operations of the base level,
            self.ops.append((       # information about nested operations is included in the used list.
                node,
                self.used))
            self.used = []


class ImportParser(Parser):
    """Find import statement.

    A parser which inherits from the basic parser to find package imports.
    """

    def __init__(self):
        self.imports = {}

    def visit_Import(self, node):
        for imp in node.names:
            self.imports[imp.name] = imp.asname

    def visit_ImportFrom(self, node):
        for imp in node.names:
            self.imports[node.module + "." + imp.name] = imp.asname


class FunctionParser(Parser):
    """Find function calls.

    A parser which inherits from the basic parser to find function calls.
    Function calls inside control structures are not found, nesting function calls are.
    """

    def __init__(self):
        self.current = ''
        self.mappings = {}
        self.calls = {}
        self.call_lookup_active = False

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Assign(self, node):
        self.visit(node.value)

    def visit_AugAssign(self, node):
        self.visit(node.value)

    def visit_Compare(self, node):
        self.visit_each(node.comparators)

    def visit_UnaryOp(self, node):
        self.visit(node.operand)

    def visit_Import(self, node):
        for imp in node.names:
            if imp.asname is not None:
                self.mappings[imp.asname] = imp.name
            else:
                pass # e.g. numpy import as numpy, so no action needed.

    def visit_ImportFrom(self, node):
        for imp in node.names:
            if imp.asname is not None:
                self.mappings[imp.asname] = node.module + "." + imp.name
            else:
                self.mappings[imp.name] = node.module + "." + imp.name

    def visit_Expr(self, node):
        self.visit(node.value)

    def visit_Call(self, node):
        if self.call_lookup_active:
            self.visit(node.func)
        else :
            self.call_lookup_active = True
            self.visit(node.func) # Need to visit func to start recording the current function name.

            if self.current:
                if (self.current not in self.calls):
                    self.calls[self.current] = []

                self.calls[self.current].append((node, node.args, node.keywords))

            self.current = ''
            self.call_lookup_active = False

            # dive deeper in func, args and keywords
            self.visit(node.func)

            for arg in node.args:
                self.visit(arg)

            for key in node.keywords:
                self.visit(key.value)


    def visit_Attribute(self, node):
        self.visit(node.value)  # Go deeper for the package/module names!
        self.current += "." + node.attr  # Add the function name

    def visit_Name(self, node):
        self.current = (node.id if not node.id in self.mappings else self.mappings[node.id])

class ObjectAccessParser(FunctionParser):
    """Find object accesses

    A parser which inherits from the FunctionParser to find object accesses.
    """

    def __init__(self):
        super().__init__()
        self.accesses = []

    def visit_Call(self, node):
        for arg in node.args:
            self.visit(arg)

        for key in node.keywords:
            self.visit(key.value)

    def visit_List(self, node):
        for el in node.elts:
            self.visit(el)

    def visit_Tuple(self, node):
        for el in node.elts:
            self.visit(el)

    def visit_Attribute(self, node):
        # if already a chain, prepend, else initialize self.current
        self.current = node.attr + "." + self.current if self.current else node.attr
        self.visit(node.value)

    def visit_Name(self, node):
        # if name refers to an import, replace
        prefix = None
        if node.id in self.mappings:
            prefix = self.mappings[node.id]
        else:
            prefix = node.id
        self.current = prefix + "." + self.current if self.current else prefix
        self.accesses.append(self.current)
        self.current = ''

class ObjectAssignmentParser(Parser):
    """Find object assignmnts

    A parser which inherits from the basic parser to find object assignments.
    All assignments at top-level, as well as in if, while, for and with statements are found.
    """

    def __init__(self):
        self.assignments = {}
        self.active_assignment = None

    def visit_Name(self, node):
        if node.id not in self.assignments:
            self.assignments[node.id] = [self.active_assignment]
        else:
            self.assignments[node.id].append(self.active_assignment)
        self.active_node = None

    def visit_Attribute(self, node):
        self.visit(node.value)

    def visit_Assign(self, node):
        self.active_assignment = node
        self.visit_each(node.targets)

    def visit_AugAssign(self, node):
        self.active_assignment = node
        self.visit(node.target)

    def visit_If(self, node):
        self.visit_each(node.body)
        self.visit_each(node.orelse)

    def visit_While(self, node):
        self.visit_each(node.body)
        self.visit_each(node.orelse)

    def visit_For(self, node):
        self.visit_each(node.body)
        self.visit_each(node.orelse)

    def visit_With(self, node):
        self.visit_each(node.body)

    def visit_Try(self, node):
        self.visit_each(node.body)
        self.visit_each(node.finalbody)

    def visit_TryFinally(self, node):
        self.visit_each(node.body)
        self.visit_each(node.finalbody)

class IfParser(Parser):
    """Find if structures.

    A parser which inherits from the basic parser to find if structures.
    Only 'top-level' if structures will be found!
    """

    def __init__(self):
        self.ifs = []

    def visit_If(self, node):
        self.ifs.append((
            node.test,
            node.body,
            node.orelse))


class WhileParser(Parser):
    """Find while structures.

    A parser which inherits from the basic parser to find while structures.
    Only 'top-level' while structures will be found!
    """

    def __init__(self):
        self.whiles = []

    def visit_While(self, node):
        self.whiles.append((
            node.test,
            node.body,
            node.orelse))


class ForParser(Parser):
    """Find for structures.

    A parser which inherits from the basic parser to find for structures.
    Only 'top-level' for structures will be found!
    """

    def __init__(self):
        self.fors = []

    def visit_For(self, node):
        self.fors.append((
            Parser.get_target_vars(node.target),
            node.iter,
            node.body,
            node.orelse))



class FunctionDefParser(Parser):
    """Find function definitions

    A parser which inherits from the basic parser to find function definitions.
    Only 'top-level' for structures will be found!
    """
    def __init__(self):
        self.defs = {}

    def visit_FunctionDef(self, node):
        args = [arg.arg for arg in node.args.args]
        defaults = [FunctionDefParser.get_node_literal_value(lit) for lit in node.args.defaults]
        defaults = [None] * (len(args) - len(defaults)) + defaults
        self.defs[node.name] = {
            "fundef": node,
            "args": [(arg, default) for arg, default in zip(args,defaults)],
            "body": FunctionBodyTransformer().visit(ast.Module(node.body)),
        }

    def get_node_literal_value(node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.Str) or isinstance(node, ast.Bytes):
            return node.s

class LambdaFunctionParser(Parser):
    """Find lambda functions

    A parser which inherits from the basic parser to find lambda functions.
    """

    def __init__(self):
        self.funs = []

    def visit_Assign(self, node):
        self.visit(node.value)

    def visit_AugAssign(self, node):
        self.visit(node.value)

    def visit_Call(self, node):
        self.visit(node.func)
        for arg in node.args:
            self.visit(arg)
        for key in node.keywords:
            self.visit(key.value)

    def visit_If(self, node):
        self.visit_each(node.body)
        self.visit_each(node.orelse)

    def visit_While(self, node):
        self.visit_each(node.body)
        self.visit_each(node.orelse)

    def visit_For(self, node):
        self.visit_each(node.body)
        self.visit_each(node.orelse)

    def visit_With(self, node):
        self.visit_each(node.body)

    def visit_Try(self, node):
        self.visit_each(node.body)
        self.visit_each(node.finalbody)

    def visit_TryFinally(self, node):
        self.visit_each(node.body)
        self.visit_each(node.finalbody)

    def visit_Lambda(self, node):
        args = [arg.arg for arg in node.args.args]
        defaults = [FunctionDefParser.get_node_literal_value(lit) for lit in node.args.defaults]
        defaults = [None] * (len(args) - len(defaults)) + defaults
        self.funs.append({
                "fun": node,
                "args": [(arg, default) for arg, default in zip(args,defaults)],
                "body": node.body
            })


class CompParser(Parser):
    def __init__(self):
        self.comps = []

    def visit_Assign(self, node):
        self.visit(node.value)

    def visit_AugAssign(self, node):
        self.visit(node.value)

    def visit_Try(self, node):
        self.visit_each(node.body)
        self.visit_each(node.finalbody)

    def visit_TryFinally(self, node):
        self.visit_each(node.body)
        self.visit_each(node.finalbody)

    def build_comp(self, node):
        target = node.generators[0].target
        self.comps.append({
                "list_comp": node,
                "body": node.elt,
                "target": target,
                "target_vars": Parser.get_target_vars(target),
                "iter": node.generators[0].iter,
                "ifs": node.generators[0].ifs
            })

class ListCompParser(CompParser):
    """Find list comprehensions

    A parser which inherits from the CompParser to find list comprehensions.
    """
    def visit_ListComp(self, node):
        self.build_comp(node)


class GeneratorExpParser(CompParser):
    """Find generator expressions

    A parser which inherits from the CompParser to find generator expressions.
    """

    def visit_GeneratorExp(self, node):
        self.build_comp(node)

class DictCompParser(CompParser):
    """Find dictionary comprehensions

    A parser which inherits from the CompParser to find dict comprehensions.
    """
    def visit_DictComp(self, node):
        target = node.generators[0].target
        self.comps.append({
                "list_comp": node,
                "key": node.key,
                "value": node.value,
                "target": target,
                "target_vars": Parser.get_target_vars(target),
                "iter": node.generators[0].iter,
                "ifs": node.generators[0].ifs
            })


class FunctionBodyTransformer(ast.NodeTransformer):
    # TODO this does not automatically contain line_end information!
    def visit_Nonlocal(self, node):
        new_node = ast.copy_location(Global(names = node.names), node)
        return FunctionBodyTransformer.decorate(new_node, node)

    def visit_Return(self, node):
        new_node = ast.copy_location(ast.Pass(), node)
        return FunctionBodyTransformer.decorate(new_node, node)

    def decorate(new_node, node):
        try:
            # only possible on the student side!
            new_node.end_lineno = node.end_lineno
            new_node.end_col_offset = node.end_col_offset
        except:
            pass
        return new_node

class WithParser(Parser):
    def __init__(self):
        self.withs = []

    def visit_With(self, node):
        items = node.items
        self.withs.append({
            "context": [{"context_expr" : ast.Expression(item.context_expr),
                "optional_vars": item.optional_vars and WithParser.get_node_ids_in_list(item.optional_vars)} for item in items],
            "body": node.body,
            "node": node
        })

    def get_node_ids_in_list(node):
        if isinstance(node, ast.Name):
            node_ids = [node.id]
        elif isinstance(node, ast.Tuple):
            node_ids = [name.id for name in node.elts]
        else:
            node_ids = []
        return node_ids

class TryExceptParser(Parser):
    def __init__(self):
        self.try_excepts = []

    def visit_Try(self, node):
        handlers = {}

        for handler in node.handlers:
            if handler.type is None:
                handlers['all'] = handler
            elif isinstance(handler.type, ast.Name):
                handlers[handler.type.id] = handler
            elif isinstance(handler.type, ast.Tuple):
                for el in handler.type.elts:
                    handlers[el.id] = handler
            else:
                # do nothing, don't know what to do!
                pass

        self.try_excepts.append({
            "try_except": node,
            "body": node.body,
            "orelse": node.orelse,
            "finalbody": node.finalbody,
            "handlers": handlers
        })

