def shorten_str(text, to_chars=100):
    return (text if len(text) <= 100 else (
        text[:(to_chars // 2)] + "..." + text[-(to_chars // 2):]))

from types import ModuleType
import copy

def get_ord(num):
    assert num != 0, "use strictly positive numbers in get_ord()"
    nums = {1: "first", 2: "second", 3:"third", 4:"fourth",
            5: "fifth", 6: "sixth", 7:"seventh", 8:"eight",
            9: "nineth", 10: "tenth"}
    if num in nums:
        return(nums[num])
    else:
        return("%dth" % num)

def get_times(num):
    nums = {1:"once", 2:"twice"}
    if num in nums:
        return(nums[num])
    else:
        return("%d times" % num)

def copy_env(env, keep_objs=None):
    if keep_objs is None:
        keep_objs = []
    mutableTypes = (tuple, list, dict)
    # One list comprehension to filter list. Might need some cleaning, but it
    # works
    update_env = {
        key: copy.deepcopy(value) for key,
        value in env.items() if not (
            key.startswith("_") or isinstance(
                value,
                ModuleType) or key in [
                'In',
                'Out',
                'get_ipython',
                'quit',
                'exit']) and (
                    key in keep_objs or isinstance(
                        value,
                        mutableTypes))}
    updated_env = dict(env)
    updated_env.update(update_env)
    return(updated_env)


def first_lower(s):
    return (s[:1].lower() + s[1:] if s else '')

def check_str(x):
    assert isinstance(x, str), "object isn't string where string expected"
    return(x)

def check_dict(x):
    assert isinstance(x, dict), "object isn't dict where dict expected"
    return(x)