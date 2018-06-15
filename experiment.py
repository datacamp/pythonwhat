from pythonbackend.Exercise import Exercise

code = """
# Import the random module
import random
# Generate random predictions
random_predictions = [random.uniform(0,1) for i in range(len(targets_test))]
random_predictions = [(r,1-r) for r in random_predictions]
"""
data = {
    "DC_PEC": """
import pandas as pd
import random
targets_test = pd.read_csv("https://s3.amazonaws.com/assets.datacamp.com/production/course_7066/datasets/Y_test.csv")
random.seed(123)
""",
    "DC_CODE":code,
    "DC_SOLUTION":code,
    "DC_SCT":"""
Ex().has_import("random")

# Check first list comprehension
Ex().check_list_comp(0).multi(
    check_iter().has_equal_value(copy = False),
    check_body().check_function("random.uniform").check_args(0).has_equal_value(copy = False)
    )

# Check second list comprehension
Ex().check_list_comp(1).multi(
    check_iter().has_equal_value(copy = False),
    check_body().set_context(r = .2).has_equal_value(copy = False)
)
"""
}

ex = Exercise(data)
ex.runInit(data)
ex.runSubmit(data)