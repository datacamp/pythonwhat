import pprint as pp
import itertools
import inspect
from functools import partial
from collections import OrderedDict

TEST_NAMES = [
    "test_mc",
    "test_or",
    "test_with",
    "test_list_comp",
    "test_dict_comp",
    "test_generator_exp",
    "test_import",
    "test_object",
    "test_correct",
    "test_if_else",
    "test_if_exp",
    "test_for_loop",
    "test_function",
    "test_print",
    "test_function_v2",
    "test_operator",
    "test_try_except",
    "test_data_frame",
    "test_dictionary",
    "test_while_loop",
    "test_student_typed",
    "test_object_accessed",
    "test_output_contains",
    "test_lambda_function",
    "test_expression_result",
    "test_expression_output",
    "test_function_definition",
    "test_object_after_expression"
]

SUB_TESTS = {
    "test_if_else": ['test', 'body', 'orelse'],
    "test_if_exp": ['test', 'body', 'orelse'],
    "test_list_comp": ['comp_iter', 'body', 'ifs'],
    "test_dict_comp": ['comp_iter', 'key', 'value', 'ifs'],
    "test_correct": ['check', 'diagnose'],
    "test_generator_exp": ['comp_iter', 'body', 'ifs'],
    "test_for_loop": ['for_iter', 'body', 'orelse'],
    "test_try_except": ['body', 'handlers', 'orelse', 'finalbody'],
    "test_while_loop": ['test', 'body', 'orelse'],
    "test_with": ['context_tests', 'body'],
    "test_function_definition": ['body'],
    "test_or": ['tests'],
    "test_lambda_function": ['body']
}

class Tree(object):
    def __init__(self):
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
        self.parent = None
        self.name = name
        self.arg_name = arg_name
        self.child_list = [] if child_list is None else child_list
        self.data = {} if data is None else data
        # hacky way to add their argument name when a function of tests was given
        self._add_child_callback = None

    def __call__(self):
        ba = self.data['bound_args']
        self.data['func'](*ba.args, **ba.kwargs)

    def partial(self):
        return partial(self.data['func'], **self.data['bound_args'].arguments)

    def update_child_calls(self):
        for node in filter(lambda n: len(n.arg_name), self.child_list):
            self.data['bound_args'].arguments[node.arg_name] = node.partial()

    def remove_child(self, node):
        indx = self.child_list.index(node)
        del self.child_list[indx]
        return indx

    def serialize(self):
        return [[c.serialize() for c in self.child_list], self.data]

    def add_child(self, child):
        # since it is a tree, there is only one parent 
        # note this means we do not allow edges between same layer units
        if child.parent: child.parent.remove_child(child)
        child.parent = self
        self.child_list.append(child)
        if self._add_child_callback: self._add_child_callback(child)

    @property
    def depth(self):
        if self.parent: return self.parent.depth + 1
        else: return 0

    def __str__(self):
        # TODO print function signature without defaults (or with)
        return pp.pformat(self.data)

    def __iter__(self):
        for c in self.child_list: yield c

class NodeList(Node):
    def partial(self):
        return [node.partial() for node in self.child_list]

    def update_child_calls(self):
        pass

class NodeDict(Node):
    def partial(self):
        return OrderedDict((node.arg_name, node.partial()) for node in self.child_list)

    def update_child_calls(self):
        pass

class Probe(object):
    def __init__(self, tree, f):
        self.tree = tree
        self.f = f
        self.test_name = f.__name__
        # TODO: auto sub_test detection
        self.sub_tests = SUB_TESTS.get(self.test_name) or []
    
    def __call__(self, *args, **kwargs):
        # st in kwargs
        bound_args = inspect.signature(self.f).bind(*args, **kwargs)
        par_names = list(bound_args.signature.parameters.keys())

        data = dict(
                bound_args = bound_args, 
                par_names= par_names, 
                func = self.f)
        this_node = Node(data=data, name=self.test_name)
        self.tree.crnt_node.add_child(this_node)

        da = bound_args.arguments
        for st in self.sub_tests:     # TODO: auto sub test detection
            if st in da and da[st]:
                self.run_sub_tests(da[st], self.tree, this_node, st)
        return this_node

    @staticmethod
    def run_sub_tests(test, tree, node, arg_name):
        # note that I've made the strong assumption that
        # if not a function, then test is a list or tuple of them
        if isinstance(test, dict):
            nd = NodeDict(name = "Dict", arg_name = arg_name)
            node.add_child(nd)
            for k, f in test.items(): Probe.run_sub_tests(f, tree, nd, k)
        elif hasattr(test, '__len__'): 
            nl = NodeList(name = "List", arg_name = arg_name)
            node.add_child(nl)
            for ii, f in enumerate(test): Probe.run_sub_tests(f, tree, nl, str(ii))
        elif isinstance(test, Node): 
            test.arg_name = arg_name
            node.add_child(test)
        elif callable(test): 
            nl = NodeList(name = "ListDeferred", arg_name = arg_name)
            node.add_child(nl)
            prev_node, tree.crnt_node = tree.crnt_node, nl
            test()
            tree.crnt_node = prev_node
        elif test is not None:
            raise Exception("Expected a function or list/dict of functions")
        


def create_test_probes(test_exercise):
    tree = Tree()
    all_tests = [test_exercise[s] for s in TEST_NAMES]
    new_context = {f.__name__: Probe(tree, f) for f in all_tests} 
    new_context.update({k:v for k,v in test_exercise.items() if k not in new_context})
    #new_context['success_msg'] =  lambda s: s
    return tree, new_context
