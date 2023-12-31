"""Assignment 2: Trees for Treemap

=== CSC148 Fall 2020 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module Description ===
This module contains the basic tree interface required by the treemap
visualiser. You will both add to the abstract class, and complete a
concrete implementation of a subclass to represent files and folders on your
computer's file system.
"""

from __future__ import annotations
import os
from random import randint
import math

from typing import Tuple, List, Optional


class AbstractTree:
    """A tree that is compatible with the treemap visualiser.

    This is an abstract class that should not be instantiated directly.

    You may NOT add any attributes, public or private, to this class.
    However, part of this assignment will involve you adding and implementing
    new public *methods* for this interface.

    === Public Attributes ===
    data_size: the total size of all leaves of this tree.
    colour: The RGB colour value of the root of this tree.
        Note: only the colours of leaves will influence what the user sees.

    === Private Attributes ===
    _root: the root value of this tree, or None if this tree is empty.
    _subtrees: the subtrees of this tree.
    _parent_tree: the parent tree of this tree; i.e., the tree that contains
        this tree
        as a subtree, or None if this tree is not part of a larger tree.

    === Representation Invariants ===
    - data_size >= 0
    - If _subtrees is not empty, then data_size is equal to the sum of the
      data_size of each subtree.
    - colour's elements are in the range 0-255.

    - If _root is None, then _subtrees is empty, _parent_tree is None, and
      data_size is 0.
      This setting of attributes represents an empty tree.
    - _subtrees IS allowed to contain empty subtrees (this makes deletion
      a bit easier).

    - if _parent_tree is not empty, then self is in _parent_tree._subtrees
    """
    data_size: int
    colour: (int, int, int)
    _root: Optional[object]
    _subtrees: List[AbstractTree]
    _parent_tree: Optional[AbstractTree]

    def __init__(self: AbstractTree, root: Optional[object],
                 subtrees: List[AbstractTree], data_size: int = 0) -> None:
        """Initialize a new AbstractTree.

        If <subtrees> is empty, <data_size> is used to initialize this tree's
        data_size. Otherwise, the <data_size> parameter is ignored, and this
        tree's data_size is computed from the data_sizes of the subtrees.

        If <subtrees> is not empty, <data_size> should not be specified.

        This method sets the _parent_tree attribute for each subtree to self.

        A random colour is chosen for this tree.

        Precondition: if <root> is None, then <subtrees> is empty.
        """
        self._root = root
        self._subtrees = subtrees
        self._parent_tree = None
        # 1. Initialize self.colour and self.data_size,
        self.colour = (
            randint(0, 255), randint(0, 255), randint(0, 255))
        if self._subtrees == []:
            self.data_size = data_size
        else:
            data = 0
            for sub in self._subtrees:
                data += sub.data_size
                self.data_size = data
        # according to the docstring.
        # 2. Properly set all _parent_tree attributes in self._subtrees
        for subtree in self._subtrees:
            subtree._parent_tree = self

    def is_empty(self: AbstractTree) -> bool:
        """Return True if this tree is empty."""
        return self._root is None

    def generate_treemap(self: AbstractTree, rect: Tuple[int, int, int, int])\
            -> List[Tuple[Tuple[int, int, int, int], Tuple[int, int, int]]]:
        """Run the treemap algorithm on this tree and return the rectangles.

        Each returned tuple contains a pygame rectangle and a colour:
        ((x, y, width, height), (r, g, b)).

        One tuple should be returned per non-empty leaf in this tree.

        @type self: AbstractTree
        @type rect: (int, int, int, int)
            Input is in the pygame format: (x, y, width, height)
        @rtype: list[((int, int, int, int), (int, int, int))]
        """
        # Read the handout carefully to help get started identifying base cases,
        # and the outline of a recursive step.
        #
        # Programming tip: use "tuple unpacking assignment" to easily extract
        # coordinates of a rectangle, as follows.
        # x, y, width, height = rect
        if self.data_size == 0:
            return []
        if self._subtrees == []:
            return [(rect, self.colour)]
        ans = []
        x, y, width, height = rect
        if rect[2] > rect[3]:
            prevwidth = x
            for sub in self._subtrees:
                if self._subtrees.index(sub) == len(self._subtrees) - 1:
                    # print("LAST: " + str(width), str(prevwidth))
                    newwidth = x + width - prevwidth
                else:
                    newwidth = math.floor(
                        (sub.data_size / self.data_size) * width)
                r = (prevwidth, y, newwidth, height)
                # print(sub._root, r)
                prevwidth += newwidth
                ans.extend(sub.generate_treemap(r))
            return ans
        prevheight = y
        for sub in self._subtrees:
            if self._subtrees.index(sub) == len(self._subtrees) - 1:
                # print("LAST: " + str(height), str(prevheight))
                newheight = y + height - prevheight
            else:
                newheight = math.floor(
                    (sub.data_size / self.data_size) * height)
            r = (x, prevheight, width, newheight)
            # print(sub._root, r)
            prevheight += newheight
            ans.extend(sub.generate_treemap(r))
        return ans

    def get_separator(self: AbstractTree) -> str:
        """Return the string used to separate nodes in the string
        representation of a path from the tree root to a leaf.

        Used by the treemap visualiser to generate a string displaying
        the items from the root of the tree to the currently selected leaf.

        This should be overridden by each AbstractTree subclass, to customize
        how these items are separated for different data domains.
        """
        raise NotImplementedError

    def enlarge_leaf(self: FileSystemTree) -> None:
        """enlarge the leaf by 1% rounded up """
        if self._subtrees != []:
            return
        toadd = math.ceil(self.data_size * 0.01)
        self.data_size += toadd
        if self._parent_tree is None:
            return
        curr = self
        while curr._parent_tree is not None:
            curr = curr._parent_tree
            curr.data_size += toadd

    def shrink_leaf(self: FileSystemTree) -> None:
        """Shrink the leaf by 1% rounded up """
        if self._subtrees != [] or self.data_size <= 1:
            return
        tosub = math.ceil(self.data_size * 0.01)
        self.data_size -= tosub
        if self._parent_tree is None:
            return
        curr = self
        while curr._parent_tree is not None:
            curr = curr._parent_tree
            curr.data_size -= tosub

    def delete_leaf(self: FileSystemTree) -> None:
        """Delete the leaf from the tree and edit the tree accordingly """
        tosub = self.data_size
        if self._parent_tree is None:
            self.data_size = 0
            return
        deleted = self
        self._parent_tree._subtrees.remove(deleted)
        self._parent_tree.data_size -= tosub
        curr = self._parent_tree
        while curr._parent_tree is not None:
            curr = curr._parent_tree
            curr.data_size -= tosub

    def find_leaf(self, location: Tuple[int, int],
                  rect: Tuple[int, int, int, int]) -> Optional[FileSystemTree]:
        """find which leafs rectangle contains this point """
        if self.data_size == 0:
            return None
        if self._subtrees == []:
            return self.on_point(location, rect)
        # print("---FILE FOLDER, CHECKING SUBTREES")
        ans = None
        x, y, width, height = rect
        if rect[2] > rect[3]:
            prevwidth = x
            for sub in self._subtrees:
                if self._subtrees.index(sub) == len(self._subtrees) - 1:
                    newwidth = x + width - prevwidth
                else:
                    newwidth = math.floor(
                        (sub.data_size / self.data_size) * width)
                r = (prevwidth, y, newwidth, height)
                prevwidth += newwidth
                ans = sub.find_leaf(location, r)
                # print("checking ", sub._root, r)
                if ans is not None:
                    return ans
            return None
        prevheight = y
        for sub in self._subtrees:
            if self._subtrees.index(sub) == len(self._subtrees) - 1:
                newheight = y + height - prevheight
            else:
                newheight = math.floor(
                    (sub.data_size / self.data_size) * height)
            r = (x, prevheight, width, newheight)
            prevheight += newheight
            ans = sub.find_leaf(location, r)
            # print("checking ", r)
            if ans is not None:
                # print("FOUND")
                return ans
        return None

    def on_point(self, location: Tuple[int, int],
                 rect: Tuple[int, int, int, int]) -> Optional[FileSystemTree]:
        """returns whether this point is in the given rectangle or not """
        r = rect
        if r[0] <= location[0] <= r[0] + r[2] \
           and r[1] <= location[1] <= r[1] + r[3]:
            return self
        return None

    def get_directory(self: FileSystemTree) -> str:
        """return the directory for a file """
        if self._parent_tree is None:
            return self._root
        sep = self.get_separator()
        return self._parent_tree.get_directory() + sep + self._root


class FileSystemTree(AbstractTree):
    """A tree representation of files and folders in a file system.

    The internal nodes represent folders, and the leaves represent regular
    files (e.g., PDF documents, movie files, Python source code files, etc.).

    The _root attribute stores the *name* of the folder or file, not its full
    path. E.g., store 'assignments', not '/Users/David/csc148/assignments'

    The data_size attribute for regular files as simply the size of the file,
    as reported by os.path.getsize.
    """
    def __init__(self: FileSystemTree, path: str) -> None:
        """Store the file tree structure contained in the given file or folder.

        Precondition: <path> is a valid path for this computer.
        """
        # Remember that you should recursively go through the file system
        # and create new FileSystemTree objects for each file and folder
        # encountered.
        #
        # Also remember to make good use of the superclass constructor!
        root = path
        size = os.path.getsize(path)
        if os.path.isdir(path):
            subfiles = [os.path.join(path, file) for file in os.listdir(path)]
            subtrees = [FileSystemTree(file) for file in subfiles]
        else:
            subtrees = []
        AbstractTree.__init__(self, os.path.basename(root), subtrees, size)

    def get_separator(self: AbstractTree) -> str:
        """ return the separator for this tree"""
        return os.path.sep


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(
        config={
            'extra-imports': ['os', 'random', 'math'],
            'generated-members': 'pygame.*'})
