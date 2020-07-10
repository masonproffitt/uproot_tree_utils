import tempfile
import os

import numpy as np

import awkward

import uproot

from uproot_tree_utils import clone_tree


def test_scalars():
    original_file = uproot.open('tests/scalars_tree_file.root')
    tree_name = 'tree'
    original_tree = original_file[tree_name]
    new_file_name = tempfile.mkstemp(suffix='.root', dir=os.getcwd())[1]
    try:
        clone_tree(original_tree, new_file_name)
        new_file = uproot.open(new_file_name)
        new_tree = new_file[tree_name]
        assert new_tree['int_branch'].array().tolist() == [0, -1]
        assert new_tree['long_branch'].array().tolist() == [0, -2]
        assert np.allclose(new_tree['float_branch'].array(), [0.0, 3.3])
        assert np.allclose(new_tree['double_branch'].array(), [0.0, 4.4])
        assert new_tree['bool_branch'].array().tolist() == [False, True]
    finally:
        if os.path.isfile(new_file_name):
            os.remove(new_file_name)


def test_vectors():
    original_file = uproot.open('tests/vectors_tree_file.root')
    tree_name = 'tree'
    original_tree = original_file[tree_name]
    new_file_name = tempfile.mkstemp(suffix='.root', dir=os.getcwd())[1]
    try:
        clone_tree(original_tree, new_file_name)
        new_file = uproot.open(new_file_name)
        new_tree = new_file[tree_name]
        assert new_tree['int_vector_branch'].array().tolist() == [[], [-1, 2, 3], [13]]
        assert abs(new_tree['float_vector_branch'].array() - awkward.fromiter([[], [-7.7, 8.8, 9.9], [15.15]])).max().max() < 1e-5
        assert abs(new_tree['double_vector_branch'].array() - awkward.fromiter([[], [-10.10, 11.11, 12.12], [16.16]])).max().max() < 1e-5
    finally:
        if os.path.isfile(new_file_name):
            os.remove(new_file_name)


def test_event_selection_scalars():
    original_file = uproot.open('tests/scalars_tree_file.root')
    tree_name = 'tree'
    original_tree = original_file[tree_name]
    new_file_name = tempfile.mkstemp(suffix='.root', dir=os.getcwd())[1]
    try:
        clone_tree(original_tree, new_file_name, selection=[False, True])
        new_file = uproot.open(new_file_name)
        new_tree = new_file[tree_name]
        assert new_tree['int_branch'].array().tolist() == [-1]
        assert new_tree['long_branch'].array().tolist() == [-2]
        assert np.allclose(new_tree['float_branch'].array(), [3.3])
        assert np.allclose(new_tree['double_branch'].array(), [4.4])
        assert new_tree['bool_branch'].array().tolist() == [True]
    finally:
        if os.path.isfile(new_file_name):
            os.remove(new_file_name)


def test_event_selection_vectors():
    original_file = uproot.open('tests/vectors_tree_file.root')
    tree_name = 'tree'
    original_tree = original_file[tree_name]
    new_file_name = tempfile.mkstemp(suffix='.root', dir=os.getcwd())[1]
    try:
        clone_tree(original_tree, new_file_name, selection=[True, False, True])
        new_file = uproot.open(new_file_name)
        new_tree = new_file[tree_name]
        assert new_tree['int_vector_branch'].array().tolist() == [[], [13]]
        assert abs(new_tree['float_vector_branch'].array() - awkward.fromiter([[], [15.15]])).max().max() < 1e-5
        assert abs(new_tree['double_vector_branch'].array() - awkward.fromiter([[], [16.16]])).max().max() < 1e-5
    finally:
        if os.path.isfile(new_file_name):
            os.remove(new_file_name)
