"""Automatically generate names.
"""
import inspect
import re
from collections import ChainMap

from .misc import formatdoc


sep = ' '
start = 1

# Match integer between square brackets at end of string if after space
# or at beginning of string or just match end of string
numbered_patt = re.compile(r'((?<=\A\[)|(?<=\s\[))(?:\d+|)(?=\]$)|$')


def _inc_name_count_sub(match):
    count = match.group(0)

    try:
        count = int(count)
    except ValueError:  # not an int
        count = f'{sep}[{start}]'
    else:
        count = f'{count + 1}'

    return count


@formatdoc
def inc_name_count(name):
    """Increase a name's count matching `{numbered_patt}` by ``1``.

    If the name is not already numbered, append '{sep}[{start}]'.

    Parameters
    ----------
    name : str
        Original name.

    Returns
    -------
    incremented_name : str
        Numbered name incremented by ``1``.
    """
    return numbered_patt.sub(_inc_name_count_sub, name, count=1)


def magic_name(value, *, path_prefix):
    """Fetch the name of the variable with the given value passed to the calling function.

    Parameters
    ----------
    value : any
        The value of the desired variable.
    path_prefix : absolute path-like, kwonly
        The path prefixes to ignore.

    Returns
    -------
    name : str or None
        Name of the variable, if found.
    """
    frame = inspect.currentframe().f_back
    code = frame.f_code

    while code.co_filename.startswith(path_prefix):
        frame = frame.f_back
        code = frame.f_code

    varmap = ChainMap(frame.f_locals, frame.f_globals)
    names = *code.co_varnames, *code.co_names

    for name in names:
        if name.isidentifier() and name in varmap and varmap[name] is value:
            return name


def force_name_unique(name, names):
    if names.count(name) == 0:
        return name
    else:
        return force_name_unique(inc_name_count(name), names)
