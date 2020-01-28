from types import ModuleType
import copy
import os


def include_v1():
    return os.environ.get("PYTHONWHAT_V2_ONLY", "") != "1"


def v2_only():
    return not include_v1()


def shorten_str(text, to_chars=100):
    if "\n" in text or len(text) > 50:
        return None
    return text


def copy_env(env):
    mutableTypes = (tuple, list, dict)
    # One list comprehension to filter list. Might need some cleaning, but it
    # works
    ipy_ignore = ["In", "Out", "get_ipython", "quit", "exit"]
    update_env = {
        key: copy.deepcopy(value)
        for key, value in env.items()
        if not any(
            (key.startswith("_"), isinstance(value, ModuleType), key in ipy_ignore)
        )
        and isinstance(value, mutableTypes)
    }
    updated_env = dict(env)
    updated_env.update(update_env)
    return updated_env


def first_lower(s):
    return s[:1].lower() + s[1:] if s else ""


def check_str(x):
    assert isinstance(x, str), "object isn't string where string expected"
    return x


def check_dict(x):
    assert isinstance(x, dict), "object isn't dict where dict expected"
    return x


def check_process(x):
    assert "Process" in x.__class__.__name__
    return x
