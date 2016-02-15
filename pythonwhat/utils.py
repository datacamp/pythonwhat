def shorten_str(text, to_chars = 100):
	return (text if len(text) <= 100 else (text[:(to_chars//2)] + "..." + text[-(to_chars//2):]))

from types import ModuleType
import copy
def copy_env(env, keep_objs = None):
	if keep_objs is None:
		keep_objs = []
	mutableTypes = (tuple, list, dict)
	# One list comprehension to filter list. Might need some cleaning, but it works
	update_env = {key: copy.deepcopy(value) for key,value in env.items() if not (key.startswith("_") or isinstance(value, ModuleType) or key in ['In', 'Out', 'get_ipython', 'quit', 'exit']) and (key in keep_objs or isinstance(value, mutableTypes))}
	updated_env = dict(env)
	updated_env.update(update_env)
	return(updated_env)