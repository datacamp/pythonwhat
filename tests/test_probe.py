from pythonwhat import probe
import importlib
te = importlib.import_module('pythonwhat.test_exercise')


sct = """
test_function("print", 1, 
  incorrect_msg = "Use [`print()`](https://docs.python.org/3/library/functions.html#print) to print the last element of `year`, `year[-1]`.")
test_function("print", 2,
  incorrect_msg = "Use [`print()`](https://docs.python.org/3/library/functions.html#print) to print the last element of `pop`, `pop[-1]`.")

test_import("matplotlib.pyplot",
  not_imported_msg = "You can import pyplot by using `import matplotlib.pyplot`.",
  incorrect_as_msg = "You should set the correct alias for `matplotlib.pyplot`, import it `as plt`.")

msg = "Use `plt.plot(year, pop)` to plot what's instructed."
test_function("matplotlib.pyplot.plot",
  not_called_msg = msg,
  incorrect_msg = msg)

msg = "Use [`plt.show()`](http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.show) to show the plot."
test_function("matplotlib.pyplot.show",
  not_called_msg = msg,
  incorrect_msg = msg)
"""

tree, context = probe.create_test_probes(te)
exec(sct, context)

sct2 = """
test_import("pandas")
test_function("pandas.read_csv")
test_object("df")

test_object("col")
def test_for_iter():
    test_expression_result()

def test_for_body():
    def test_test():
        test_function("langs_count.keys")
    def test_body():
        test_student_typed("\+=\s*1")
    def test_orelse():
        test_student_typed("=\s*1")
    test_if_else(index = 1,
                 test = test_test,
                 body = test_body,
                 orelse = test_orelse)

test_for_loop(
    index=1,
    for_iter=test_for_iter,
    body=test_for_body
)

test_object("langs_count")
test_function("print")

success_msg("Great work!")
"""

tree2, context2 = probe.create_test_probes(te)
exec(sct2, context2)
