import os.path

import yaml
import rstcloth.rstcloth
from typing import Any, Callable, Dict, List, TypeVar, Union

T = TypeVar('T')


def compare_mtimes(target: str, dependencies: List[str]) -> bool:
    """Return True if any of the dependency paths are newer than the target
       path. Otherwise returns False."""
    try:
        target_mtime = os.path.getmtime(target)
    except FileNotFoundError:
        return True

    dependencies_mtime = max([os.path.getmtime(dep) for dep in dependencies])
    return dependencies_mtime > target_mtime


def substitute(text: str, replacements: Dict[str, str]) -> str:
    """Quick-and-dirty template substitution function."""
    for src, dest in replacements.items():
        text = text.replace('{{{{{}}}}}'.format(src), dest)

    return text


def substitute_rstcloth(cloth: rstcloth.rstcloth.RstCloth,
                        replacements: Dict[str, str]) -> str:
    return substitute('\n'.join(cloth.data), replacements)


def withdraw(dictionary: Dict[str, Any], key: str, checker: Callable[[Any], T], default: T=None) -> T:
    """Removes a value from a dictionary, after transforming it with a given
       checker function. Returns either the value, or None if it does
       not exist."""
    try:
        value = dictionary[key]
    except KeyError:
        return default

    del dictionary[key]
    if value is None:
        return None

    return checker(value)


def str_or_list(value: Union[List[str], str]) -> str:
    """Coerces a string or list of strings into a string."""
    if isinstance(value, str):
        return value

    if isinstance(value, list):
        return ', '.join(value)

    raise TypeError(value)


def string_list(value: Union[List[str], str]) -> List[str]:
    """Coerces a string or list of strings into a list of strings."""
    if isinstance(value, str):
        return [value]

    return [str(x) for x in value]


def str_dict(value: Dict[str, str]) -> Dict[str, str]:
    """Transforms a dictionary into a dictionary mapping strings to strings."""
    return dict([(str(v[0]), str(v[1]) if v[1] is not None else None) for v in value.items()])


def str_any_dict(value: Dict[str, Any]) -> Dict[str, Any]:
    """Transforms a dictionary into a dictionary mapping strings to anything."""
    return dict([(str(v[0]), v[1] if v[1] is not None else None) for v in value.items()])


def list_str_any_dict(values: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Transforms a list of dictionaries into a list of dictionaries
       mapping strings to anything."""
    return [str_any_dict(x) for x in values]


def load_yaml(path: str) -> List[Dict[str, Any]]:
    """Open a file and parse the YAML within."""
    with open(path, 'r') as f:
        return list(yaml.load_all(f, Loader=yaml.CLoader))