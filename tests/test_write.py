import tempfile
import os

import numpy as np

import uproot

from uproot_tree_utils import write_tree


def test_write():
    treename = 'tree'
    branchname = 'branch'
    original_array = np.array([1, 2, 3])
    filename = tempfile.mkstemp(suffix='.root', dir=os.getcwd())[1]
    try:
        write_tree({branchname: original_array}, filename, treename)
        file = uproot.open(filename)
        tree = file[treename]
        assert tree[branchname].array().tolist() == original_array.tolist()
    finally:
        if os.path.isfile(filename):
            os.remove(filename)
