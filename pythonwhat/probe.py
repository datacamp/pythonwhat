import pprint as pp
import itertools

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
    "test_list_comp": ['body', 'ifs'],
    "test_dict_comp": ['key', 'value', 'ifs'],
    "test_generator_exp": ['body', 'ifs'],
    "test_for_loop": ['for_iter', 'body', 'orelse'],
    "test_try_except": ['body', 'value', 'test'],
    "test_while_loop": ['test', 'body', 'orelse']
}

class Tree(object):
    def __init__(self):
        self.root = Node(name="root")
        self.crnt_node = self.root
        self.crnt_test_name = ""

    @classmethod
    def str_branch(cls, node, str_func=lambda s: ""):
        f = node.data.get('func')
        this_node =  "  "*node.depth + getattr(f, '__name__', node.name) + str_func(node) + "\n"
        return this_node + "".join(map(lambda x: cls.str_branch(x, str_func), node.child_list))

    def __str__(self):
        return self.str_branch(self.crnt_node)

    @classmethod
    def descend(cls, node=None):
        node = self.crnt_node if node is None else node
        children = map(cls.descend, node.child_list)
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
        self.data['func'](**self.data['bound_args'])

    def update_child_calls(self):
        # TODO can use count dict in collection lib?
        arg_names = set(node.arg_name for node in self.child_list)
        for name in arg_names:
            args = list(filter(lambda n: n.arg_name == name, self.child_list))
            args = args[0] if len(args) == 1 else args
            self.data['bound_args'] = args


    def serialize(self):
        return [[c.serialize() for c in self.child_list], self.data]

    def add_child(self, child):
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



class Probe(object):
    def __init__(self, tree, f):
        self.tree = tree
        self.f = f
        self.test_name = f.__name__
        self.sub_tests = SUB_TESTS.get(self.test_name) or []
    
    def __call__(self, *args, **kwargs):
        # st in kwargs
        bound_args = inspect.signature(self.f).bind(*args, **kwargs)
        par_names = list(bound_args.signature.parameters.keys())

        data = dict(
                bound_args =  bound_args.arguments, 
                par_names=par_names, 
                func = self.f)
        this_node = Node(data=data, name=self.test_name, arg_name = self.tree.crnt_test_name)
        self.tree.crnt_node.add_child(this_node)

        # TODO pointer to child_node corresponding to argument
        da = bound_args.arguments
        for st in self.sub_tests: 
            if st in da and da[st]:
                self.run_sub_tests(da[st], self.tree, this_node, st)

    def run_sub_tests(self, test, tree, node, arg_name):
        prev_node, crnt_node = tree.crnt_node, node
        tree.crnt_node = crnt_node
        tree.crnt_test_name = arg_name
        # note that I've made the strong assumption that
        # if not a function, then test is a list or tuple of them
        if callable(test): test()
        else: 
            for f in test: f()
        tree.crnt_node = prev_node
        tree.crnt_test_name = ""
        


def create_test_probes(test_exercise):
    from types import ModuleType
    tree = Tree()
    if isinstance(test_exercise, ModuleType): 
        all_tests = map(lambda s: getattr(test_exercise, s), TEST_NAMES)
    else:
        all_tests = map(lambda s: test_exercise.get(s), TEST_NAMES)
    new_context = {f.__name__: Probe(tree, f) for f in all_tests} 
    if not isinstance(test_exercise, ModuleType):
        new_context.update({k:v for k,v in test_exercise.items() if k not in new_context})
    new_context['success_msg'] =  lambda s: s
    return tree, new_context

import inspect
def match_args(f, *args, **kwargs):
    bound_args = inspect.signature(f).bind(*args, **kwargs)
    manual_args = bound_args.arguments
    bound_args.apply_defaults()

    return manual_args, bound_args.arguments
