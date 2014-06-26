# -*- coding: utf-8 -*-

# Copyright (c) 2013 Fatih Erikli
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# https://github.com/fatiherikli/dictdiffer

import copy

(ADD, REMOVE, CHANGE) = (
    'add', 'remove', 'change')


def _hashable(x):
    """type(x) must be a list.
    if items in list are all hashable return True, else return False.
    """
    for i in x:
        if not i.__hash__:
            return False
    return True


def diff(first, second, node=None, list_order=True,nodel=False):
    """
    Compares two dictionary object, and returns a diff result.

    if list_order is False and if the list`s subitems are hashable,
    the subitem`s order will be ignored.

        >>> result = diff({'a':'b'}, {'a':'c'})
        >>> list(result)
        [('change', 'a', ('b', 'c'))]
        >>> a = {'a': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]}
        >>> b = {'a': [0, 1, 2, 123, 4, 5, 6, 7, 8, 9]}
        >>> list(diff(a, b))
        [('change', 'a.3', (3, 123))]
        >>> list(diff(a, b, list_order=False))
        [('add', 'a', [123]), ('remove', 'a', [3])]

    """
    node = node or []
    dotted_node = '.'.join(node)
    ignore_list_diff = False

    if isinstance(first, dict):
        # dictionaries are not hashable, we can't use sets
        intersection = [k for k in first if k in second]
        addition = [k for k in second if not k in first]
        deletion = [k for k in first if not k in second]
    elif isinstance(first, list):
        if list_order is True or not (_hashable(first) or _hashable(second)):
            len_first = len(first)
            len_second = len(second)
            intersection = range(0, min(len_first, len_second))
            addition = range(min(len_first, len_second), len_second)
            deletion = range(min(len_first, len_second), len_first)
        else:
            set_first = set(first)
            set_second = set(second)
            intersection = set_first.intersection(set_second)
            addition = set_second.difference(set_first)
            deletion = set_first.difference(set_second)
            ignore_list_diff = True

    def diff_dict_list():
        """Compares if object is a dictionary. Callees again the parent
        function as recursive if dictionary have child objects.
        Yields `add` and `remove` flags."""
        for key in intersection:
            # if type is not changed, callees again diff function to compare.
            # otherwise, the change will be handled as `change` flag.

            # if ignore list order, the intersection of two list means no diff.
            if ignore_list_diff:
                continue
            recurred = diff(
                first[key],
                second[key],
                node=node + [str(key) if isinstance(key, int) else key],
                list_order=list_order)

            for diffed in recurred:
                yield diffed

        if addition:
            if list_order is True:
                yield ADD, dotted_node, [
                    # for additions, return a list that consist with
                    # two-pair tuples.
                    (key, second[key]) for key in addition]
            else:
                # return a list that consist with two-pair tuples.
                # the tuples consist with a empty list and the additions list.
                yield ADD, dotted_node, list(addition)
          
        if deletion:
            if nodel:
                yield
            if list_order is True:
                yield REMOVE, dotted_node, [
                    # for deletions, return the list of removed keys
                    # and values.
                    (key, first[key]) for key in deletion]
            else:
                # return a list that consist with two-pair tuples.
                # the tuples consist with the deletions list and a empty list.
                yield REMOVE, dotted_node, list(deletion)

    def diff_otherwise():
        """Compares string and integer types. Yields `change` flag."""
        if first != second:
            yield CHANGE, dotted_node, (first, second)

    differs = {
        dict: diff_dict_list,
        list: diff_dict_list,
    }

    differ = differs.get(type(first))
    return (differ or diff_otherwise)()


def patch(diff_result, destination, set_remove=True):
    """
    Patches the diff result to the old dictionary.
    """
    destination = copy.deepcopy(destination)

    def add(node, changes):
        for key, value in changes:
            dest = dot_lookup(destination, node)
            if isinstance(dest, list):
                dest.insert(key, value)
            else:
                dest[key] = value

    def change(node, changes):
        dest = dot_lookup(destination, node, parent=True)
        last_node = node.split('.')[-1]
        if isinstance(dest, list) or last_node not in dest:
            last_node = int(last_node)
        _, value = changes
        dest[last_node] = value

    def remove(node, changes):
        for key, _ in changes:
            del dot_lookup(destination, node)[key]

    patchers = {
        REMOVE: remove,
        ADD: add,
        CHANGE: change
    }

    for action, node, changes in diff_result:
        if action == "remove" and set_remove is False:
            continue
        patchers[action](node, changes)

    return destination


def swap(diff_result):
    """
    Swaps the diff result with the following mapping

        * pull -> push
        * push -> pull
        * remove -> add
        * add -> remove

    In addition, swaps the changed values for `change` flag.

        >>> swapped = swap([('add', 'a.b.c', ('a', 'b'))])
        >>> next(swapped)
        ('remove', 'a.b.c', ('a', 'b'))

        >>> swapped = swap([('change', 'a.b.c', ('a', 'b'))])
        >>> next(swapped)
        ('change', 'a.b.c', ('b', 'a'))

    """

    def add(node, changes):
        return REMOVE, node, changes

    def remove(node, changes):
        return ADD, node, changes

    def change(node, changes):
        first, second = changes
        return CHANGE, node, (second, first)

    swappers = {
        REMOVE: remove,
        ADD: add,
        CHANGE: change
    }

    for action, node, change in diff_result:
        yield swappers[action](node, change)


def revert(diff_result, destination):
    """
    A helper function that calles swap function to revert
    patched dictionary object.

        >>> first = {'a': 'b'}
        >>> second = {'a': 'c'}
        >>> revert(diff(first, second), second)
        {'a': 'b'}

    """
    return patch(swap(diff_result), destination)


def dot_lookup(source, lookup=None, parent=False):
    """
    A helper function that allows you to reach dictionary
    items with dot lookup (e.g. document.properties.settings)

        >>> dot_lookup({'a': {'b': 'hello'}}, 'a.b')
        'hello'

    If parent argument is True, returns the parent node of matched
    object.

        >>> dot_lookup({'a': {'b': 'hello'}}, 'a.b', parent=True)
        {'b': 'hello'}

    If node is empty value, returns the whole dictionary object.

        >>> dot_lookup({'a': {'b': 'hello'}}, '')
        {'a': {'b': 'hello'}}

    """
    if lookup is None:
        return source

    value = source
    if type(lookup) == int:
        try:
            return value[lookup]
        except (IndexError, KeyError):
            raise RuntimeError("Item Found Failed: %s[%s]" % (source, lookup))

    keys = lookup.split('.')
    if parent:
        keys = keys[:-1]
    for key in keys:
        if isinstance(value, list) or key not in value:
            key = int(key)
        value = value[key]
    return value


def diff_with_primary_key(first, second, primary_key):
    """
    Compares two list that using dictionary as their subitems,
    confirm the diff type(add, remove, change) by primary key,
    and returns a diff result.


        >>> a = [{"a": "b", "k": "v"}]
        >>> b = [{"a": "c", "k": "v"}]
        >>> c = [{"a": "b", "k": "value"}]
        >>> result = diff_with_primary_key(a, b, "a")
        >>> list(result)
        [('remove', '', {'a': 'b', 'k': 'v'}), ('add', '', {'a': 'c', 'k': 'v'})]
        >>> result = diff_with_primary_key(a, c, "a")
        >>> list(result)
        [('change', '', {'a': 'b', 'k': 'value'})]

    """
    if not isinstance(first, list) or not isinstance(second, list):
        raise RuntimeError("The data to be compared must be list.")
    try:
        init_pk = set(i[primary_key] for i in first)
        new_pk = set(i[primary_key] for i in second)
    except TypeError:
        raise RuntimeError("The subitem must be a dict.")
    except KeyError:
        raise RuntimeError("Primary key not found.")
    del_items = init_pk.difference(new_pk)
    add_items = new_pk.difference(init_pk)
    change_items = init_pk.intersection(new_pk)
    for i in first:
        if i[primary_key] in del_items:
            yield "remove", "", i
    for i in second:
        if i[primary_key] in add_items:
            yield "add", "", i
        elif i[primary_key] in change_items and i not in first:
            yield "change", "", i
