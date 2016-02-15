import ast
from pythonwhat.parsing import IfParser

ip = IfParser()
tree = ast.parse('''
if True:
	print("this is true")
elif False:
	print("this is false")
else:
	print("false aswell")
if True:
	print("second true!")
''')
ast.dump(tree)
ip.visit(tree)
ip.ifs


from pythonwhat.State import State

state = State("student code","solution code", {"a": None}, {"b": None}, "the output")
state.to_child_state(None, None)






import ast
from pythonwhat.parsing import ForParser

fp = ForParser()
tree = ast.parse('''
for i in [1, 2, 3]:
	print(i)
''')
ast.dump(tree)
fp.visit(tree)
fp.fors


from pythonwhat.State import State

state = State("student code","solution code", {"a": None}, {"b": None}, "the output")
state.to_child_state(None, None)



import ast
from pythonwhat.parsing import OperatorParser

op = OperatorParser()
tree = ast.parse('''
for i in range(0, 5):
	print(i)
''')
ast.dump(tree)
op.visit(tree)
op.ops
