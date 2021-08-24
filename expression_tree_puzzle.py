"""
=== Module Description ===

This module contains the ExpressionTreePuzzle class.
"""

from __future__ import annotations

from typing import List, Dict

from expression_tree import ExprTree
from puzzle import Puzzle


class ExpressionTreePuzzle(Puzzle):
    """"
    An expression tree puzzle.

    === Public Attributes ===
    variables: the dictionary of variable name (str) - value (int) pairs
               A variable is considered "unassigned" unless it has a
               non-zero value.
    target: the target value for the expression tree to evaluate to

    === Private Attributes ===
    _tree: the expression tree

    === Representation Invariants ===
    - variables contains a key for each variable appearing in _tree

    - all values stored in variables are single digit integers (0-9).
    """
    _tree: ExprTree
    variables: Dict[str, int]
    target: int

    def __init__(self, tree: ExprTree, target: int) -> None:
        """
        Create a new expression tree puzzle given the provided
        expression tree and the target value. The variables are initialized
        using the tree's populate_lookup method.

        >>> puz = ExpressionTreePuzzle(ExprTree('a', []), 4)
        >>> puz.variables == {'a': 0}
        True
        >>> puz.target
        4
        """

        self.variables = {}
        tree.populate_lookup(self.variables)
        self._tree = tree
        self.target = target

    def is_solved(self) -> bool:
        """
        Return True iff ExpressionTreePuzzle self is solved.

        The puzzle is solved if all variables have been assigned a non-zero
        value and the expression tree evaluates to the target value.

        >>> exp_t = ExprTree('+', [ExprTree('a', []), ExprTree('b', [])])
        >>> puz = ExpressionTreePuzzle(exp_t, 7)
        >>> puz.is_solved()
        False
        >>> puz.variables['a'] = 7
        >>> puz.is_solved()
        False
        >>> puz.variables['a'] = 5
        >>> puz.variables['b'] = 2
        >>> puz.is_solved()
        True
        """
        if self._tree.is_empty():
            return False
        for key in self.variables:
            if self.variables[key] == 0:
                return False
        return self._tree.eval(self.variables) == self.target

    def __str__(self) -> str:
        """
        Return a string representation of this ExpressionTreePuzzle.

        The first line should show the dictionary of variables and the
        second line should show the string representation of the algebraic
        equation represented by the puzzle.

        >>> exprt = ExprTree('+', [ExprTree('*', \
                                            [ExprTree('a', []), \
                                             ExprTree('+', [ExprTree('b', []), \
                                                            ExprTree(6, []), \
                                                            ExprTree(6, []), \
                                                           ])]), \
                                   ExprTree(5, [])])
        >>> puz = ExpressionTreePuzzle(exprt, 61)
        >>> print(puz)
        {'a': 0, 'b': 0}
        ((a * (b + 6 + 6)) + 5) = 61
        """
        c = '{'
        for key in self.variables:
            c += "'" + key + "': " + str(self.variables[key]) + ', '
        c = c[:len(c) - 2] + '}' + '\n'
        c += self._tree.__str__() + ' = ' + str(self.target)
        return c

    def extensions(self) -> List[ExpressionTreePuzzle]:
        """
        Return the list of legal extensions of this ExpressionTreePuzzle.

        A legal extension is a new ExpressionTreePuzzle equal to this
        ExpressionTreePuzzle, except that it assigns a single currently
        unassigned variable a value in the range 1-9.

        A variable is "unassigned" if it has a value of 0.

        A copy of the expression tree and variables dictionary should be
        used in each extension made, so as to avoid unintended aliasing.

        >>> exp_t = ExprTree('a', [])
        >>> puz = ExpressionTreePuzzle(exp_t, 7)
        >>> exts_of_puz = puz.extensions()
        >>> len(exts_of_puz) == 9
        True
        >>> exts_of_an_ext = exts_of_puz[0].extensions()
        >>> len(exts_of_an_ext) == 0
        True
        >>> exp_t = ExprTree('a', [ExprTree('b', [])])
        >>> puz = ExpressionTreePuzzle(exp_t, 8)
        >>> exts_of_puz = puz.extensions()
        >>> len(exts_of_puz) == 18
        True
        """
        extensions = []
        c = []
        for key in self.variables:
            if isinstance(key, str) and self.variables[key] == 0:
                c.append(key)
        for ele in c:
            for k in range(1, 10):
                tree = ExpressionTreePuzzle(self._tree, self.target)
                d = self.variables.copy()
                d[ele] = k
                tree.variables = d
                extensions.append(tree)
        return extensions


    def fail_fast(self) -> bool:
        """
        Return True if this ExpressionTreePuzzle can be quickly determined to
        have no solution, False otherwise.

        """

        if self._tree.eval(self.variables) > self.target:
            return True
        else:
            return False


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    import python_ta

    python_ta.check_all(config={'pyta-reporter': 'ColorReporter',
                                'allowed-io': [],
                                'allowed-import-modules': ['doctest',
                                                           'python_ta',
                                                           'typing',
                                                           '__future__',
                                                           'expression_tree',
                                                           'puzzle'],
                                'disable': ['E1136'],
                                'max-attributes': 15}
                        )
