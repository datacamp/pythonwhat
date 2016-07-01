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

    The basic Parser, should not be used on itself but should be used to inherit certain basic
    features from. The Parser itself inherits from ast.Nodevisitor, which is a helper class to
    go through the abstract syntax tree objects.

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
            # does not now about the State object.
            self.visit(line)


    def visit_Expression(self, node):
        """
        This function is called when a Expression node is encountered when traversing the tree.

        Args:
            node (ast.Expression): The node which is visited.
        """
        self.visit(node.body)

    def generic_visit(self, node):
        """
        This function is called when all other nodes are encountered when traversing the tree.
        When inheriting form this standard parser, this function will make the parser ignore
        all nodes that are not relevant to build its data structures.

        Args:
            node (ast.Node): The node which is visited.
        """
        pass  # This ignore is necessary to keep the parser at base level, also look comment above in
              # the visit_Module function body.


class OperatorParser(Parser):
    """Find operations.

    A parser which inherits from the basic parser. It will walk through the syntax tree and put all
    operators in a relevant data structure, which can later be used in the test.

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
        """
        This function is called when a Expr node is encountered when traversing the tree.

        Args:
            node (ast.Expr): The node which is visited.
        """
        self.visit(node.value)

    def visit_Call(self, node):
        """
        This function is called when a Call node is encountered when traversing the tree.

        Args:
            node (ast.Call): The node which is visited.
        """
        for arg in node.args:
            self.visit(arg)

    def visit_Assign(self, node):
        """
        This function is called when a Assign node is encountered when traversing the tree.

        Args:
            node (ast.Assign): The node which is visited.
        """
        self.visit(node.value)

    def visit_Num(self, node):
        """
        This function is called when a Num node is encountered when traversing the tree.

        Args:
            node (ast.Num): The node which is visited.
        """
        if not self.level:
            self.ops.append((  # A number can be seen as a operator on base level.
                node.lineno,   # When student is asked to use operators but just puts in a number instead,
                node,          # this will help creating a consistent feedback message,
                self.used))

    def visit_UnaryOp(self, node):
        """
        This function is called when a UnaryOp node is encountered when traversing the tree.

        Args:
            node (ast.UnaryOp): The node which is visited.
        """
        self.visit(
            node.operand)  # Unary operations, like '-', should not be added, but they should be
        # looked into. They can contain more binary operations. This is important
        # during the nesting process.

    def visit_BinOp(self, node):
        """
        This function is called when a BinOp node is encountered when traversing the tree.

        Args:
            node (ast.BinOp): The node which is visited.
        """
        self.used.append(OperatorParser.O_MAP[type(node.op).__name__])
        self.level = self.level + 1
        # Nest to other operations, but increase the level. We only
        self.visit(node.left)
        # want to now which operations are used at a deeper level, but
        self.visit(node.right)
        self.level = self.level - 1  # we don't need all the explicit nodes.

        if not self.level:          # We should only add the binary operations of the base level,
            self.ops.append((       # information about nested operations is included in the used
                node.lineno,        # list.
                node,
                self.used))
            self.used = []


class BoolParser(Parser):
    """Find boolean operations.

    A parser which inherits from the basic parser. It will walk through the syntax tree and put all
    boolean operators in a relevant data structure, which can later be used in the test.

    Attributes:
        bools (list()): A list containing the correct data structure.
    """

    def __init__(self):
        """
        Initialize the parser and its attributes.
        """
        self.bools = []


class ImportParser(Parser):
    """Find import statement.

    A parser which inherits from the basic parser. It will walk through the syntax tree and put all
    import statements in a relevant data structure, which can later be used in the test.

    Attributes:
        imports (dict()): A dict containing the correct data structure.
    """

    def __init__(self):
        """
        Initialize the parser and its attributes.
        """
        self.imports = {}

    def visit_Import(self, node):
        """
        This function is called when an Import node is encountered when traversing the tree.

        Args:
            node (ast.Import): The node which is visited.
        """
        for imp in node.names:
            self.imports[imp.name] = imp.asname

    def visit_ImportFrom(self, node):
        """
        This function is called when an ImportFrom node is encountered when traversing the tree.

        Args:
            node (ast.ImportFrom): The node which is visited.
        """
        for imp in node.names:
            self.imports[node.module + "." + imp.name] = imp.asname


class FunctionParser(Parser):
    """Find function calls.

    A parser which inherits from the basic parser. It will walk through the syntax tree and put all
    function calls in a relevant data structure, which can later be used in the test.

    Attributes:
        current (str): The function call which is being constructed, important for dotted function calls.
        calls (dict(str: list(tuple(num, list(ast.Node), list(keyword))))):
            A dictionary containing the function names as a key, and a list of structured tuples as value. The tuples
            contain information about the line number, the arguments and the keywords of each call.
    """

    def __init__(self):
        """
        Initialize the parser and its attributes.
        """
        self.current = ''
        self.imports = {} # We need to keep track of imports to match the correction function calls
        self.calls = {}

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_Assign(self, node):
        self.visit(node.value)

    def visit_AugAssign(self, node):
        self.visit(node.value)

    def visit_UnaryOp(self, node):
        self.visit(node.operand)

    def visit_Import(self, node):
        for imp in node.names:
            if imp.asname is not None:
                self.imports[imp.asname] = imp.name

    def visit_ImportFrom(self, node):
        for imp in node.names:
            if imp.asname is not None:
                self.imports[imp.asname] = node.module + "." + imp.name

    def visit_Expr(self, node):
        """
        This function is called when a Expr node is encountered when traversing the tree.

        Args:
            node (ast.Expr): The node which is visited.
        """
        self.visit(node.value)

    def visit_Call(self, node):
        """
        This function is called when a Call node is encountered when traversing the tree.

        Args:
            node (ast.Call): The node which is visited.
        """
        self.visit(
            node.func)       # Need to visit func to start recording the current function name.

        if self.current:
            if (self.current not in self.calls):
                self.calls[self.current] = []

            self.calls[self.current].append(
                (node.lineno, node.args, node.keywords))

        self.current = ''
        for arg in node.args:
            # Need to visit all argument nodes for nested functions.
            self.visit(arg)

        for key in node.keywords:
            self.visit(key.value)   # Same for keywords

    def visit_Attribute(self, node):
        """
        This function is called when a Attribute node is encountered when traversing the tree.

        Args:
            node (ast.Attribute): The node which is visited.
        """
        self.visit(
            node.value)          # Go deeper for the package/module names!
        self.current += "." + node.attr   # Add the function name

    def visit_Name(self, node):
        """
        This function is called when a Name node is encountered when traversing the tree.

        Args:
            node (ast.Name): The node which is visited.
        """
        self.current = (
            node.id if not node.id in self.imports else self.imports[
                node.id])

class ObjectAccessParser(FunctionParser):
    """Find object accesses

    A parser which inherits from the FunctionParser. It will walk through the syntax tree and put all
    object accesses in a list, which can later be used in the test.
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
        if self.current:
            self.current = node.attr + "." + self.current
        else:
            self.current = node.attr
        self.visit(node.value)

    def visit_Name(self, node):
        if self.current:
            self.current = node.id + "." + self.current
        else:
            self.current = node.id

        self.accesses.append(self.current)
        self.current = ''


class IfParser(Parser):
    """Find if structures.

    A parser which inherits from the basic parser. It will walk through the syntax tree and put all
    function calls in a relevant data structure, which can later be used in the test.

    Attributes:
        current (str): The function call which is being constructed, important for dotted function calls.
        calls (dict(str: list(tuple(num, list(ast.Node), list(keyword))))):
            A dictionary containing the function names as a key, and a list of structured tuples as value. The tuples
            contain information about the line number, the arguments and the keywords of each call.
    """

    def __init__(self):
        """
        Initialize the parser and its attributes.
        """
        self.ifs = []

    def visit_If(self, node):
        """
        This function is called when a If node is encountered when traversing the tree.

        Args:
            node (ast.If): The node which is visited.
        """
        self.ifs.append((
            node.lineno,
            node.test,
            ast.Module(node.body),
            ast.Module(node.orelse)))


class WhileParser(Parser):

    def __init__(self):
        self.whiles = []

    def visit_While(self, node):
        self.whiles.append((
            node.lineno,
            node.test,
            ast.Module(node.body),
            ast.Module(node.orelse)))


class ForParser(Parser):
    """Find for structures.

    A parser which inherits from the basic parser. It will walk through the syntax tree and put all
    for calls in a relevant data structure, which can later be used in the test.

    Attributes:
        current (str): The function call which is being constructed, important for dotted function calls.
        calls (dict(str: list(tuple(num, list(ast.Node), list(keyword))))):
            A dictionary containing the function names as a key, and a list of structured tuples as value. The tuples
            contain information about the line number, the arguments and the keywords of each call.
    """

    def __init__(self):
        """
        Initialize the parser and its attributes.
        """
        self.fors = []

    def visit_For(self, node):
        """
        This function is called when a For node is encountered when traversing the tree.

        Args:
            node (ast.For): The node which is visited.
        """
        if isinstance(node.target, ast.Name):
            target_vars = [node.target.id]
        elif isinstance(node.target, ast.Tuple):
            target_vars = [name.id for name in node.target.elts]
        else:
            target_vars = []

        self.fors.append((
            node.lineno,
            target_vars,
            node.iter,
            ast.Module(node.body),
            ast.Module(node.orelse)))

class FunctionDefParser(Parser):
    def __init__(self):
        self.defs = {}

    def visit_FunctionDef(self, node):
        args = [arg.arg for arg in node.args.args]
        defaults = [FunctionDefParser.get_node_literal_value(lit) for lit in node.args.defaults]
        defaults = [None] * (len(args) - len(defaults)) + defaults
        self.defs[node.name] = {
            "args": [(arg, default) for arg, default in zip(args,defaults)],
            "body": ReturnTransformer().visit(ast.Module(node.body)),
            "lineno": node.lineno
        }

    def get_node_literal_value(node):
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.Str) or isinstance(node, ast.Bytes):
            return node.s

class ReturnTransformer(ast.NodeTransformer):
    def visit_Return(self, node):
        return ast.copy_location(ast.Pass(), node)

class WithParser(Parser):
    def __init__(self):
        self.withs = []

    def visit_With(self, node):
        items = node.items
        self.withs.append({
            "context": [{"context_expr" : ast.Expression(item.context_expr),
                "optional_vars": item.optional_vars and WithParser.get_node_ids_in_list(item.optional_vars)} for item in items],
            "body": ast.Module(node.body),
            "lineno": node.lineno
        })

    def get_node_ids_in_list(node):
        if isinstance(node, ast.Name):
            node_ids = [node.id]
        elif isinstance(node, ast.Tuple):
            node_ids = [name.id for name in node.elts]
        else:
            node_ids = []
        return node_ids

class FindLastLineParser(ast.NodeVisitor):
    """Find the last line.

    Search the last line number of a code part.
    """
    def __init__(self):
        self.last_line = 0

    def generic_visit(self, node):
        if hasattr(node, 'lineno') and node.lineno > self.last_line:
            self.last_line = node.lineno

        ast.NodeVisitor.generic_visit(self, node)
