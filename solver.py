"""
=== Module Description ===

This module contains the abstract Solver class and its two subclasses, which
find solutions to puzzles, step by step.
"""

from __future__ import annotations
from typing import List, Optional, Set

from adts import Queue

from puzzle import Puzzle


class Solver:
    """"
    A solver for full-information puzzles. This is an abstract class
    and purely provides the interface for our solve method.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        raise NotImplementedError


class DfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a depth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        if puzzle.is_solved():
            return [puzzle]
        elif puzzle.fail_fast():
            return []
        if seen is None:
            seen = set()
        seen.add(puzzle.__str__())
        for extension in puzzle.extensions():
            if extension.__str__() not in seen:
                b = self.solve(extension, seen)
                if len(b) != 0:
                    a = [puzzle]
                    a.extend(b)
                    return a
        return []


class BfsSolver(Solver):
    """"
    A solver for full-information puzzles that uses
    a breadth first search strategy.
    """

    def solve(self, puzzle: Puzzle,
              seen: Optional[Set[str]] = None) -> List[Puzzle]:
        """
        Return a list of puzzle states representing a path to a solution of
        <puzzle>. The first element in the list should be <puzzle>, the
        second element should be a puzzle that is in <puzzle>.extensions(),
        and so on. The last puzzle in the list should be such that it is in a
        solved state.

        In other words, each subsequent item of the returned list should take
        the puzzle one step closer to a solution, which is represented by the
        last item in the list.

        Return an empty list if the puzzle has no solution.

        <seen> is either None (default) or a set of puzzle states' string
        representations, whose puzzle states can't be any part of the path to
        the solution.
        """
        if puzzle.fail_fast():
            return []
        q = Queue()
        q.enqueue([puzzle])
        if seen is None:
            seen = set()
        seen.add(puzzle.__str__())
        while not q.is_empty():
            a = q.dequeue()
            if a[-1].is_solved():
                return a
            r = a[-1].extensions()
            for b in r:
                if b.__str__() not in seen and not b.fail_fast():
                    seen.add(b.__str__())
                    c = a.copy()
                    c.append(b)
                    q.enqueue(c)
        return []


if __name__ == "__main__":
    import python_ta

    python_ta.check_all(config={'pyta-reporter': 'ColorReporter',
                                'allowed-io': [],
                                'allowed-import-modules': ['doctest',
                                                           'python_ta',
                                                           'typing',
                                                           '__future__',

                                                           'puzzle',
                                                           'adts'],
                                'disable': ['E1136'],
                                'max-attributes': 15}
                        )
