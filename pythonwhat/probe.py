import pprint as pp
import itertools
import inspect
from functools import partial
from collections import OrderedDict
from pythonwhat import test_funcs

TEST_NAMES = [
    "test_mc",
    "test_or",
    "test_with",
    "test_import",
    "test_object",
    "test_correct",
    "test_if_else",
    "test_for_loop",
    "test_function",
    "test_list_comp",
    "test_function_v2",
    "test_data_frame",
    "test_while_loop",
    "test_student_typed",
    "test_object_accessed",
    "test_output_contains",
    "test_expression_result",
    "test_expression_output",
    "test_function_definition",
    "test_object_after_expression"
]

SUB_TESTS = {
    "test_if_else": ['test', 'body', 'orelse'],
    "test_list_comp": ['comp_iter', 'body', 'ifs'],
    "check_correct": ['check', 'diagnose'],
    "test_for_loop": ['for_iter', 'body', 'orelse'],
    "test_while_loop": ['test', 'body', 'orelse'],
    "test_with": ['context_tests', 'body'],
    "test_function_definition": ['body'],
    "check_or": ['tests']
}

class Tree(object):
    def __init__(self):
        """
        Represent a tree of nodes, by holding the currently active node.

        This class is necessary to put sub-tests onto a graph, because they may
        exist inside of function calls. By getting the currently active node
        from the tree, Probe instances may add subtests as children on that node,
        and update it when recursing over sub-tests.
        
        """
        self.root = Node(name="root")
        self.crnt_node = self.root

    @classmethod
    def str_branch(cls, node, str_func=lambda s: ""):
        f = node.data.get('func')
        this_node =  "  "*node.depth + getattr(f, '__name__', node.name) + str_func(node) + "\n"
        return this_node + "".join(map(lambda x: cls.str_branch(x, str_func), node.child_list))

    def __str__(self):
        return self.str_branch(self.crnt_node)

    def descend(self, node=None):
        node = self.crnt_node if node is None else node
        children = map(self.descend, node.child_list)
        base = [node] if node.name != "root" else []
        return sum(children, base)

    def __iter__(self):
        for ii in self.descend(self.crnt_node): yield ii

class Node(object):
    def __init__(self, child_list = None, data = None, name="unnamed", arg_name=""):
        """
        Hold a function call with its bound arguments, along with child nodes.
        
        """
        self.parent = None
        self.name = name
        self.arg_name = arg_name
        self.child_list = [] if child_list is None else child_list
        self.data = {} if data is None else data
        self.updated = False
        # hacky way to add their argument name when a function of tests was given

    def __call__(self, state=None):
        """Call original function with its arguments, and optional state"""
        ba = self.data['bound_args']
        if state:
            self.data['func'](state=state, *ba.args, **ba.kwargs)
            return state
        else:
            self.data['func'](*ba.args, **ba.kwargs)
            ba.apply_defaults()
            return ba.arguments['state']

    def __str__(self):
        # TODO print function signature without defaults (or with)
        return pp.pformat(self.data)

    def __iter__(self):
        for c in self.child_list: yield c

    def partial(self):
        """Return partial of original function call"""
        ba = self.data['bound_args']
        return partial(self.data['func'], *ba.args, **ba.kwargs)

    def update_child_calls(self):
        """Replace child nodes on original function call with their partials"""

        for node in filter(lambda n: len(n.arg_name), self.child_list):
            self.data['bound_args'].arguments[node.arg_name] = node.partial()
        self.updated = True

    def remove_child(self, node):
        indx = self.child_list.index(node)
        del self.child_list[indx]
        return indx

    def add_child(self, child):
        # since it is a tree, there is only one parent 
        # note this means we do not allow edges between same layer units
        if child.parent: child.parent.remove_child(child)
        child.parent = self
        self.child_list.append(child)

    def descend(self, include_me=True):
        """Descend depth first into all child nodes"""
        if include_me: yield self

        for child in self.child_list:
            yield child
            yield from child.descend()

    @property
    def depth(self):
        if self.parent: return self.parent.depth + 1
        else: return 0

class NodeList(Node):
    def partial(self):
        return [node.partial() for node in self.child_list]

    def update_child_calls(self):
        pass

class Probe(object):
    def __init__(self, tree, f, eval_on_call=False):
        self.tree = tree
        self.f = f
        self.test_name = f.__name__
        self.eval_on_call = eval_on_call
        # TODO: auto sub_test detection
        self.sub_tests = SUB_TESTS.get(self.test_name) or []
    
    def __call__(self, *args, **kwargs):
        """Bind arguments to original function signature, and store in a Node

        This is used to discover what tests and sub-tests the SCT would like to 
        call, and defer them for later execution via their node instance. Node
        instances are assembled into a tree.

        """

        bound_args = inspect.signature(self.f).bind(*args, **kwargs)

        data = dict(
                bound_args = bound_args, 
                func = self.f)
        this_node = Node(data=data, name=self.test_name)
        if self.tree is not None:
            self.tree.crnt_node.add_child(this_node)

        # First pass to set up branches off node
        da = bound_args.arguments
        for st in self.sub_tests:     # TODO: auto sub test detection
            if st in da and da[st]:
                self.build_sub_test_nodes(da[st], self.tree, this_node, st)

        # Second pass to build node and all its children into a subtest
        for node in this_node.descend(include_me=True):
            if node.updated:         # already built, e.g. node used multiple times
                continue
            else:
                node.update_child_calls()
        
        if self.eval_on_call: return this_node()
        else:                 return this_node

    @staticmethod
    def build_sub_test_nodes(test, tree, node, arg_name):
        # note that I've made the strong assumption that
        # if not a function, then test is a dict, list or tuple of them
        if isinstance(test, (list, tuple)): 
            nl = NodeList(name = "List", arg_name = arg_name)
            node.add_child(nl)
            for ii, f in enumerate(test): Probe.build_sub_test_nodes(f, tree, nl, str(ii))
        elif isinstance(test, Node):
            # test was a lambdaless subtest call, which produced a node
            # so need to tell it what its arg_name was on parent test
            test.arg_name = arg_name
            node.add_child(test)
        elif callable(test):
            # test was inside a lambda, function containing subtests or v2 F() chain object with subtests
            # since either may contain multiple subtests, we put them in a node list
            nl = NodeList(name = "ListDeferred", arg_name = arg_name)
            node.add_child(nl)
            if tree is not None:
                prev_node, tree.crnt_node = tree.crnt_node, nl
                test()
                tree.crnt_node = prev_node
            else:
                test()
        elif test is not None:
            raise Exception("Expected a function or list/tuple/dict of functions")


def build_probe_context():
    tree = Tree()
    probe_context = {s: Probe(tree, getattr(test_funcs, s)) for s in TEST_NAMES}
    return tree, probe_context
