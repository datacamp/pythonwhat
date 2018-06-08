# Changelog

All notable changes to the `pythonwhat` project will be documented in this file. This project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## 2.12.1

### Added

- Reference documentation now contains examples for `set_context()` and `set_env()`.
- A `tests/test_debug.py` file has been added to easily test questions that CDs might have.

### Changed

- There was a bug in the feedback message generation for errors. It now just refers to the console.


## 2.12.0

### Added

- All new `has_()` functions are now properly documented, so there should be no reason for you to use a `test_` function other than `test_or` and `test_correct`. If you do find yourself using it (because you don't know the alternative), ping me and we'll talk!
- Added documentation on the `check_function_def()` related functions.
- `index = 0` is now a default for functions like `check_if_else()`, `check_function()` etc.
- Like there is `set_context`, there is now `set_env` to set environment variables before using something like `has_equal_value()`. These `set_` functions serve as alternatives for the `extra_env` and `context_vals` arguments that appear in many functions and that I plan to discontinue at some point.
- Added a `test_` to `check_` article, that explains how you can go from old-style to new-style SCTs. Feel free to contribute!!

### Changed

- If you experiment locally, you will now see the feedback message that the SCT chain would generate (this is explained in the README on GitHub):

```Python
from pythonwhat.local import setup_state
s = setup_state(sol_code = "x = 4", stu_code = "x = 5")
s.check_object('x').has_equal_value()
# <traceback omitted>
# pythonwhat.Test.TestFail: Check the variable `x`. Unexpected expression value: expected `4`, got `5`.
```

- The glossary is featured more prominently in the docs, as it is a good resource to see how everything fits together.

### Removed

- There is no support for `keep_objs_in_env`, as nobody is using it.