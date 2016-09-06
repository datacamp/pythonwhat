# THIS IS CODE COPIED FROM THE thonny project https://bitbucket.org/plas/thonny
# MIT license

import ast
import _ast
import io
import sys
import token
import tokenize
import traceback

class Record:
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def update(self, **kw):
        self.__dict__.update(kw)

    def setdefault(self, **kw):
        "updates those fields that are not yet present (similar to dict.setdefault)"
        for key in kw:
            if not hasattr(self, key):
                setattr(self, key, kw[key])

    def __repr__(self):
        keys = self.__dict__.keys()
        items = ("{}={!r}".format(k, self.__dict__[k]) for k in keys)
        return "{}({})".format(self.__class__.__name__, ", ".join(items))

    def __str__(self):
        keys = sorted(self.__dict__.keys())
        items = ("{}={!r}".format(k, str(self.__dict__[k])) for k in keys)
        return "{}({})".format(self.__class__.__name__, ", ".join(items))

    def __eq__(self, other):
        if type(self) != type(other):
            return False

        if len(self.__dict__) != len(other.__dict__):
            return False

        for key in self.__dict__:
            if not hasattr(other, key):
                return False
            self_value = getattr(self, key)
            other_value = getattr(other, key)

            if type(self_value) != type(other_value) or self_value != other_value:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(repr(self))

class TextRange(Record):
    def __init__(self, lineno, col_offset, end_lineno, end_col_offset):
        self.lineno = lineno
        self.col_offset = col_offset
        self.end_lineno = end_lineno
        self.end_col_offset = end_col_offset

    def contains_smaller(self, other):
        this_start = (self.lineno, self.col_offset)
        this_end = (self.end_lineno, self.end_col_offset)
        other_start = (other.lineno, other.col_offset)
        other_end = (other.end_lineno, other.end_col_offset)

        return (this_start < other_start and this_end > other_end
                or this_start == other_start and this_end > other_end
                or this_start < other_start and this_end == other_end)

    def contains_smaller_eq(self, other):
        return self.contains_smaller(other) or self == other

    def not_smaller_in(self, other):
        return not other.contains_smaller(self)

    def is_smaller_in(self, other):
        return other.contains_smaller(self)

    def not_smaller_eq_in(self, other):
        return not other.contains_smaller_eq(self)

    def is_smaller_eq_in(self, other):
        return other.contains_smaller_eq(self)

    def get_start_index(self):
        return str(self.lineno) + "." + str(self.col_offset)

    def get_end_index(self):
        return str(self.end_lineno) + "." + str(self.end_col_offset)

    def __str__(self):
        return "TR(" + str(self.lineno) + "." + str(self.col_offset) + ", " \
                     + str(self.end_lineno) + "." + str(self.end_col_offset) + ")"


def extract_text_range(source, text_range):
    lines = source.splitlines(True)
    # get relevant lines
    lines = lines[text_range.lineno-1:text_range.end_lineno]

    # trim last and first lines
    lines[-1] = lines[-1][:text_range.end_col_offset]
    lines[0] = lines[0][text_range.col_offset:]
    return "".join(lines)


def parse_source(source, filename='<unknown>', mode="exec"):
    root = ast.parse(source, filename, mode)
    mark_text_ranges(root, source)
    return root


def mark_text_ranges(node, source, debug = False):
    """
    Node is an AST, source is corresponding source as string.
    Function adds recursively attributes end_lineno and end_col_offset to each node
    which has attributes lineno and col_offset.
    """


    def _extract_tokens(tokens, lineno, col_offset, end_lineno, end_col_offset):
        return list(filter((lambda tok: tok.start[0] >= lineno
                                   and (tok.start[1] >= col_offset or tok.start[0] > lineno)
                                   and tok.end[0] <= end_lineno
                                   and (tok.end[1] <= end_col_offset or tok.end[0] < end_lineno)
                                   and tok.string != ''),
                           tokens))



    def _mark_text_ranges_rec(node, tokens, prelim_end_lineno, prelim_end_col_offset):
        """
        Returns the earliest starting position found in given tree,
        this is convenient for internal handling of the siblings
        """

        # set end markers to this node
        if "lineno" in node._attributes and "col_offset" in node._attributes:
            if debug:
                print("=======================")
                print(node.__class__.__name__)
                print(ast.dump(node))
                print("before extraction")
                print([tok.string for tok in tokens])
                print(prelim_end_lineno)
                print(prelim_end_col_offset)
                print(node.__dict__)
            tokens = _extract_tokens(tokens, node.lineno, node.col_offset, prelim_end_lineno, prelim_end_col_offset)
            if debug:
                print("before marking")
                print([tok.string for tok in tokens])
            try:
                tokens = _mark_end_and_return_child_tokens(node, tokens, prelim_end_lineno, prelim_end_col_offset)
            except:
                if debug:
                    print("BROKEN")
                else:
                    pass
                node.end_lineno = node.lineno
                node.end_col_offset = node.col_offset + 1


        # mark its children, starting from last one
        # NB! need to sort children because eg. in dict literal all keys come first and then all values
        children = list(_get_ordered_child_nodes(node))
        for child in reversed(children):
            (prelim_end_lineno, prelim_end_col_offset) = \
                _mark_text_ranges_rec(child, tokens, prelim_end_lineno, prelim_end_col_offset)

        if "lineno" in node._attributes and "col_offset" in node._attributes:
            # new "front" is beginning of this node
            prelim_end_lineno = node.lineno
            prelim_end_col_offset = node.col_offset

        return (prelim_end_lineno, prelim_end_col_offset)


    def _strip_trailing_junk_from_expressions(tokens):
        while (tokens[-1].type not in (token.RBRACE, token.RPAR, token.RSQB,
                                      token.NAME, token.NUMBER, token.STRING)
                    and not (hasattr(token, "ELLIPSIS") and tokens[-1].type == token.ELLIPSIS)
                    and tokens[-1].string not in ")}]"
                    or tokens[-1].string in ['and', 'as', 'assert', 'class', 'def', 'del',
                                              'elif', 'else', 'except', 'exec', 'finally',
                                              'for', 'from', 'global', 'if', 'import', 'in',
                                              'is', 'lambda', 'not', 'or', 'try',
                                              'while', 'with', 'yield']):
            del tokens[-1]

    def _strip_trailing_extra_closers(tokens, remove_naked_comma, careful_leveling):
        level = 0
        for i in range(len(tokens)):
            if tokens[i].string in "({[":
                level += 1
            elif tokens[i].string in ")}]":
                # in some cases, you have test)(1, 2); you still want to include the args!!
                if careful_leveling and \
                   level == 0 and \
                   tokens[i].string == ")" and \
                   len(tokens) > i + 1 and \
                   tokens[i + 1].string == "(":
                    level = 0
                else:
                    level -= 1

            if level == 0 and tokens[i].string == "," and remove_naked_comma:
                tokens[:] = tokens[0:i]
                return

            if level < 0:
                tokens[:] = tokens[0:i]
                return

    def _strip_unclosed_brackets(tokens):
        level = 0
        for i in range(len(tokens)-1, -1, -1):
            if tokens[i].string in "({[":
                level -= 1
            elif tokens[i].string in ")}]":
                level += 1

            if level < 0:
                tokens[:] = tokens[0:i]
                level = 0  # keep going, there may be more unclosed brackets

    def _mark_end_and_return_child_tokens(node, tokens, prelim_end_lineno, prelim_end_col_offset):
        """
        # shortcut
        node.end_lineno = prelim_end_lineno
        node.end_col_offset = prelim_end_col_offset
        return tokens
        """
        # prelim_end_lineno and prelim_end_col_offset are the start of
        # next positioned node or end of source, ie. the suffix of given
        # range may contain keywords, commas and other stuff not belonging to current node

        # Function returns the list of tokens which cover all its children

        if isinstance(node, _ast.stmt):
            # remove empty trailing lines
            while (tokens[-1].type in (tokenize.NL, tokenize.COMMENT, token.NEWLINE, token.INDENT)
                   or tokens[-1].string in (":", "else", "elif", "finally", "except")):
                del tokens[-1]

        else:
            if debug:
                print("Before stripping")
                print([tok.string for tok in tokens])
            remove_naked_comma = not isinstance(node, (ast.Tuple, ast.Lambda, ast.Call, ast.ListComp, ast.DictComp, ast.GeneratorExp))
            careful_leveling = isinstance(node, ast.Call)
            _strip_trailing_extra_closers(tokens, remove_naked_comma, careful_leveling)
            if debug:
                print("After trailing extra closers")
                print([tok.string for tok in tokens])
            _strip_trailing_junk_from_expressions(tokens)
            if debug:
                print("After trailing junk")
                print([tok.string for tok in tokens])
            _strip_unclosed_brackets(tokens)
            if debug:
                print("After unclosed brackets")
                print([tok.string for tok in tokens])

        # set the end markers of this node
        node.end_lineno = tokens[-1].end[0]
        node.end_col_offset = tokens[-1].end[1]

        # Peel off some trailing tokens which can't be part any
        # positioned child node.
        # TODO: maybe cleaning from parent side is better than
        # _strip_trailing_junk_from_expressions

        # Remove trailing empty parens from no-arg call
        if (isinstance(node, ast.Call)
            and _tokens_text(tokens[-2:]) == "()"):
            del tokens[-2:]

        # Remove trailing full slice
        elif isinstance(node, ast.Subscript):
            if  _tokens_text(tokens[-3:]) == "[:]":
                del tokens[-3:]

            elif _tokens_text(tokens[-4:]) == "[::]":
                del tokens[-4:]

        # Attribute name would confuse the "value" of Attribute
        elif isinstance(node, ast.Attribute):
            assert tokens[-1].type == token.NAME
            del tokens[-1]
            _strip_trailing_junk_from_expressions(tokens)

        return tokens

    debug = debug
    all_tokens = list(tokenize.tokenize(io.BytesIO(source.encode('utf-8')).readline))
    source_lines = source.splitlines(True)
    fix_ast_problems(node, source_lines, all_tokens)
    prelim_end_lineno = len(source_lines)
    prelim_end_col_offset = len(source_lines[len(source_lines)-1])
    _mark_text_ranges_rec(node, all_tokens, prelim_end_lineno, prelim_end_col_offset)


def fix_ast_problems(tree, source_lines, tokens):
    # Problem 1:
    # Python parser gives col_offset as offset to its internal UTF-8 byte array
    # I need offsets to chars
    utf8_byte_lines = list(map(lambda line: line.encode("UTF-8"), source_lines))

    # Problem 2:
    # triple-quoted strings have just plain wrong positions: http://bugs.python.org/issue18370
    # Fortunately lexer gives them correct positions
    string_tokens = list(filter(lambda tok: tok.type == token.STRING, tokens))

    # Problem 3:
    # Binary operations have wrong positions: http://bugs.python.org/issue18374

    # Problem 4:
    # Function calls have wrong positions in Python 3.4: http://bugs.python.org/issue21295
    # similar problem is with Attributes and Subscripts

    def fix_node(node):
        for child in _get_ordered_child_nodes(node):
        #for child in ast.iter_child_nodes(node):
            fix_node(child)

        if isinstance(node, ast.Str):
            # fix triple-quote problem
            # get position from tokens
            token = string_tokens.pop(0)
            node.lineno, node.col_offset = token.start

        elif ((isinstance(node, ast.Expr) or isinstance(node, ast.Attribute))
            and isinstance(node.value, ast.Str)):
            # they share the wrong offset of their triple-quoted child
            # get position from already fixed child
            # TODO: try whether this works when child is in parentheses
            node.lineno = node.value.lineno
            node.col_offset = node.value.col_offset

        elif (isinstance(node, ast.BinOp)
            and compare_node_positions(node, node.left) > 0):
            # fix binop problem
            # get position from an already fixed child
            node.lineno = node.left.lineno
            node.col_offset = node.left.col_offset

        elif (isinstance(node, ast.Call)
            and compare_node_positions(node, node.func) > 0):
            # Python 3.4 call problem
            # get position from an already fixed child
            node.lineno = node.func.lineno
            node.col_offset = node.func.col_offset

        elif (isinstance(node, ast.Attribute)
            and compare_node_positions(node, node.value) > 0):
            # Python 3.4 attribute problem ...
            node.lineno = node.value.lineno
            node.col_offset = node.value.col_offset

        elif (isinstance(node, ast.Subscript)
            and compare_node_positions(node, node.value) > 0):
            # Python 3.4 Subscript problem ...
            node.lineno = node.value.lineno
            node.col_offset = node.value.col_offset

        else:
            # Let's hope this node has correct lineno, and byte-based col_offset
            # Now compute char-based col_offset
            if hasattr(node, "lineno"):
                byte_line = utf8_byte_lines[node.lineno-1]
                char_col_offset = len(byte_line[:node.col_offset].decode("UTF-8"))
                node.col_offset = char_col_offset


    fix_node(tree)

def compare_node_positions(n1, n2):
    if n1.lineno > n2.lineno:
        return 1
    elif n1.lineno < n2.lineno:
        return -1
    elif n1.col_offset > n2.col_offset:
        return 1
    elif n2.col_offset < n2.col_offset:
        return -1
    else:
        return 0

def _get_ordered_child_nodes(node):
    if isinstance(node, ast.Dict):
        children = []
        for i in range(len(node.keys)):
            children.append(node.keys[i])
            children.append(node.values[i])
        return children
    elif isinstance(node, ast.Call):
        children = [node.func] + node.args

        for kw in node.keywords:
            children.append(kw.value)

        # TODO: take care of Python 3.5 updates (eg. args=[Starred] and keywords)
        if hasattr(node, "starargs") and node.starargs is not None:
            children.append(node.starargs)
        if hasattr(node, "kwargs") and node.kwargs is not None:
            children.append(node.kwargs)

        children.sort(key=lambda x: (x.lineno, x.col_offset))
        return children

    elif isinstance(node, ast.arguments):
        children = node.args + node.kwonlyargs + node.kw_defaults + node.defaults

        if node.vararg is not None:
            children.append(node.vararg)
        if node.kwarg is not None:
            children.append(node.kwarg)

        children.sort(key=lambda x: (x.lineno, x.col_offset))
        return children

    else:
        return ast.iter_child_nodes(node)

def _tokens_text(tokens):
    return "".join([t.string for t in tokens])


## ADDED BY FILIP
def extract_text_from_node(dastring, astobj):
    try:
        if issubclass(type(astobj), _ast.Module):
            astobj = astobj.body
        if isinstance(astobj, list) and len(astobj) > 0:
            rangeobj = TextRange(lineno=astobj[0].lineno,
                                 col_offset=astobj[0].col_offset,
                                 end_lineno=astobj[-1].end_lineno,
                                 end_col_offset=astobj[-1].end_col_offset)
        else:
            rangeobj = TextRange(lineno=astobj.lineno,
                                 col_offset=astobj.col_offset,
                                 end_lineno=astobj.end_lineno,
                                 end_col_offset=astobj.end_col_offset)
        return(extract_text_range(dastring, rangeobj))
    except:
        return("")


## PRETTY PRINT FROM GREEN TREE SNAKES
"""
A pretty-printing dump function for the ast module.  The code was copied from
the ast.dump function and modified slightly to pretty-print.

Alex Leone (acleone ~AT~ gmail.com), 2010-01-30

From http://alexleone.blogspot.co.uk/2010/01/python-ast-pretty-printer.html
"""

from ast import *

def dump(node, annotate_fields=True, include_attributes=False, indent='  '):
    """
    Return a formatted dump of the tree in *node*.  This is mainly useful for
    debugging purposes.  The returned string will show the names and the values
    for fields.  This makes the code impossible to evaluate, so if evaluation is
    wanted *annotate_fields* must be set to False.  Attributes such as line
    numbers and column offsets are not dumped by default.  If this is wanted,
    *include_attributes* can be set to True.
    """
    def _format(node, level=0):
        if isinstance(node, AST):
            fields = [(a, _format(b, level)) for a, b in iter_fields(node)]
            if include_attributes and node._attributes:
                fields.extend([(a, _format(getattr(node, a), level))
                               for a in node._attributes])
            return ''.join([
                node.__class__.__name__,
                '(',
                ', '.join(('%s=%s' % field for field in fields)
                           if annotate_fields else
                           (b for a, b in fields)),
                ')'])
        elif isinstance(node, list):
            lines = ['[']
            lines.extend((indent * (level + 2) + _format(x, level + 2) + ','
                         for x in node))
            if len(lines) > 1:
                lines.append(indent * (level + 1) + ']')
            else:
                lines[-1] += ']'
            return '\n'.join(lines)
        return repr(node)

    if not isinstance(node, AST):
        raise TypeError('expected AST, got %r' % node.__class__.__name__)
    return _format(node)

def parseprint(code, filename="<string>", mode="exec", **kwargs):
    """Parse some code from a string and pretty-print it."""
    node = parse(code, mode=mode)   # An ode to the code
    print(dump(node, **kwargs))

# Short name: pdp = parse, dump, print
pdp = parseprint
