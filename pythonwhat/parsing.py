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

    @staticmethod
    def get_arg(el):
        if el is None:
            return None
        else :
            return el.arg

    @staticmethod
    def get_arg_tuples(arguments, defaults):
        arguments = [arg.arg for arg in arguments]
        defaults = [None] * (len(arguments) - len(defaults)) + defaults
        return list(zip(arguments, defaults))

    @staticmethod
    def get_arg_parts(arguments, defaults, name=None):
        # only difference is that it doesn't pull out arg.arg, so we can 
        # use all the information on the arg node down the road
        match_def = [None] * (len(arguments) - len(defaults)) + defaults
        part_list = []
        for _arg, _def in zip(arguments, match_def):
            part_list.append(Parser.get_arg_part(_arg, _def))
        return part_list

    @staticmethod
    def get_arg_part(_arg, _def, name=None):
        if not _arg: return None

        return {
                'node': _def or _arg,
                'arg': _arg,
                # TODO: need to fill out
                'type': 'default' if _def else 'positional',
                'is_default': True if _def else False,
                'name': name or _arg.arg,
                'annotation': _arg.annotation
                }


class OperatorParser(Parser):
    """Find operations.

    A parser which inherits from the basic parser to find binary operators.

    Attributes:
        out (list(tuple(num, ast.BinOp, list(str)))): A list of tuples containing the linenumber, node and list of used binary operations.
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
        self.out = []
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
            self.out.append((  # A number can be seen as a operator on base level.
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
            self.out.append((       # information about nested operations is included in the used list.
                node,
                self.used))
            self.used = []


class ImportParser(Parser):
    """Find import statement.

    A parser which inherits from the basic parser to find package imports.
    """

    def __init__(self):
        self.out = {}

    def visit_Import(self, node):
        for imp in node.names:
            self.out[imp.name] = imp.asname

    def visit_ImportFrom(self, node):
        for imp in node.names:
            self.out[node.module + "." + imp.name] = imp.asname


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
        self.out = []

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
        self.out.append(self.current)
        self.current = ''

class ObjectAssignmentParser(Parser):
    """Find object assignmnts

    A parser which inherits from the basic parser to find object assignments.
    All assignments at top-level, as well as in if, while, for and with statements are found.
    """

    def __init__(self):
        self.out = {}
        self.active_assignment = None

    def visit_Name(self, node):
        if self.active_assignment is not None:
            if node.id not in self.out:
                self.out[node.id] = [self.active_assignment]
            else:
                self.out[node.id].append(self.active_assignment)
            self.active_assignment = None

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
        self.out = []

    def visit_If(self, node):
        self.out.append({
            'node': node,
            'test': node.test,
            'body': node.body,
            'orelse': node.orelse,
            })


class IfExpParser(IfParser):
    """Find if structures.

    A parser which inherits from the basic parser to find inline if structures.
    Only 'top-level' if structures will be found!
    """

    def visit_If(self, node): return

    def visit_IfExp(self, node):
        super().visit_If(node)

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

    def visit_Expr(self, node):
        self.visit(node.value)

    def visit_Call(self, node):
        self.visit(node.func)

    def visit_Return(self, node):
        self.visit(node.value)


class WhileParser(Parser):
    """Find while structures.

    A parser which inherits from the basic parser to find while structures.
    Only 'top-level' while structures will be found!
    """

    def __init__(self):
        self.out = []

    def visit_While(self, node):
        self.out.append({
            'node': node,
            'test': node.test,
            'body': node.body,
            'orelse': node.orelse
            })


class ForParser(Parser):
    """Find for structures.

    A parser which inherits from the basic parser to find for structures.
    Only 'top-level' for structures will be found!
    """

    def __init__(self):
        self.out = []

    def visit_For(self, node):
        self.out.append({
            'node': node,
            'iter': node.iter,
            'body': node.body,
            'orelse': node.orelse,
            'target': node.target,
            'target_vars': Parser.get_target_vars(node.target)
            })


class FunctionDefParser(Parser):
    """Find function definitions

    A parser which inherits from the basic parser to find function definitions.
    Only 'top-level' for structures will be found!
    """
    def __init__(self):
        self.out = {}

    def visit_FunctionDef(self, node):
        self.out[node.name] = self.parse_node(node)


    @classmethod
    def parse_node(cls, node):
        normal_args = cls.get_arg_tuples(node.args.args, node.args.defaults)
        kwonlyargs = cls.get_arg_tuples(node.args.kwonlyargs, node.args.kw_defaults)
        # TODO: all single args should be tuples like this
        vararg = cls.get_arg(node.args.vararg)
        kwarg =  cls.get_arg(node.args.kwarg)
        # create context variables
        target_vars = [arg[0] for arg in normal_args]
        if vararg: target_vars.append(vararg)
        if kwarg:  target_vars.append(kwarg)
        
        return {
            "node": node,
            "args": {'args': normal_args, 'kwonlyargs': kwonlyargs, 'vararg': vararg, 'kwarg': kwarg},
            # TODO: arg is the node counterpart to target_vars
            "arg": cls.get_arg_parts(node.args.args, node.args.defaults),
            "vararg": cls.get_arg_part(node.args.vararg, None),
            "kwarg":  cls.get_arg_part(node.args.kwarg, None),
            "body": FunctionBodyTransformer().visit(ast.Module(node.body)),
            "target_vars": target_vars
        }


class LambdaFunctionParser(Parser):
    """Find lambda functions

    A parser which inherits from the basic parser to find lambda functions.
    """

    def __init__(self):
        self.out = []

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
        self.out.append(FunctionDefParser.parse_node(node))


class CompParser(Parser):
    def __init__(self):
        self.out = []

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
        self.out.append({
                "node": node,
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
        self.out.append({
                "node": node,
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
        new_node = ast.copy_location(ast.Global(names = node.names), node)
        return FunctionBodyTransformer.decorate(new_node, node)

    def visit_Return(self, node):
        new_node = ast.copy_location(ast.Expr(value = node.value), node)
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
        self.out = []

    def visit_With(self, node):
        items = node.items
        self.out.append({
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
        self.out = []

    def visit_Try(self, node):
        handlers = {}

        for handler in node.handlers:
            if isinstance(handler.type, ast.Tuple):
                # of form -- except TypeError, KeyError
                for el in handler.type.elts:
                    handlers[el.id] = self.parse_handler(handler)
            else:
                # either general handler, or single error handler
                k = 'all' if not handler.type else handler.type.id
                handlers[k] = self.parse_handler(handler)

        self.out.append({
            "node": node,
            "body": node.body,
            "orelse": node.orelse or None,
            "finalbody": node.finalbody or None,
            "handlers": handlers
        })

    @staticmethod
    def parse_handler(handler): return {
                'node': handler.body,
                'target_vars': handler.name
                }

parser_dict = {
        "object_accesses": ObjectAccessParser,
        "object_assignments": ObjectAssignmentParser,
        "operators": OperatorParser,
        "imports": ImportParser,
        "if_calls": IfParser,
        "if_exp_calls": IfExpParser,
        "while_calls": WhileParser,
        "for_calls": ForParser,
        "function_defs": FunctionDefParser,
        "lambda_functions": LambdaFunctionParser,
        "list_comps": ListCompParser,
        "dict_comps": DictCompParser,
        "generator_exps": GeneratorExpParser,
        "withs": WithParser,
        "try_excepts": TryExceptParser
}
