import tempfile
import os

import numpy as np

import awkward

import uproot

from uproot_tree_utils import clone_tree


def test_signed_integer_scalars():
    original_file = uproot.open('tests/signed_integer_scalars_tree_file.root')
    treename = 'tree'
    original_tree = original_file[treename]
    new_filename = tempfile.mkstemp(suffix='.root', dir=os.getcwd())[1]
    try:
        clone_tree(original_tree, new_filename)
        new_file = uproot.open(new_filename)
        new_tree = new_file[treename]
        assert new_tree['char_t_branch'].array().tolist() == [0, 1, -13]
        assert new_tree['short_t_branch'].array().tolist() == [0, 3, -15]
        assert new_tree['int_t_branch'].array().tolist() == [0, 5, -17]
        assert new_tree['long64_t_branch'].array().tolist() == [0, 11, -23]
    finally:
        if os.path.isfile(new_filename):
            os.remove(new_filename)


def test_floating_point_scalars():
    original_file = uproot.open('tests/floating_point_scalars_tree_file.root')
    treename = 'tree'
    original_tree = original_file[treename]
    new_filename = tempfile.mkstemp(suffix='.root', dir=os.getcwd())[1]
    try:
        clone_tree(original_tree, new_filename)
        new_file = uproot.open(new_filename)
        new_tree = new_file[treename]
        assert np.allclose(new_tree['float_t_branch'].array(), [0.0, 7.7, -19.19])
        assert np.allclose(new_tree['float16_t_branch'].array(), [0.0, 8.8, -20.20])
        assert np.allclose(new_tree['double_t_branch'].array(), [0.0, 9.9, -21.21])
        assert np.allclose(new_tree['double32_t_branch'].array(), [0.0, 10.10, -22.22])
    finally:
        if os.path.isfile(new_filename):
            os.remove(new_filename)


def test_boolean_scalars():
    original_file = uproot.open('tests/boolean_scalars_tree_file.root')
    treename = 'tree'
    original_tree = original_file[treename]
    new_filename = tempfile.mkstemp(suffix='.root', dir=os.getcwd())[1]
    try:
        clone_tree(original_tree, new_filename)
        new_file = uproot.open(new_filename)
        new_tree = new_file[treename]
        assert new_tree['bool_t_branch'].array().tolist() == [False, True, False]
    finally:
        if os.path.isfile(new_filename):
            os.remove(new_filename)


def test_vectors():
    original_file = uproot.open('tests/vectors_tree_file.root')
    treename = 'tree'
    original_tree = original_file[treename]
    new_filename = tempfile.mkstemp(suffix='.root', dir=os.getcwd())[1]
    try:
        clone_tree(original_tree, new_filename)
        new_file = uproot.open(new_filename)
        new_tree = new_file[treename]
        assert new_tree['int_vector_branch'].array().tolist() == [[], [-1, 2, 3], [13]]
        assert abs(new_tree['float_vector_branch'].array() - awkward.fromiter([[], [-7.7, 8.8, 9.9], [15.15]])).max().max() < 1e-5
        assert abs(new_tree['double_vector_branch'].array() - awkward.fromiter([[], [-10.10, 11.11, 12.12], [16.16]])).max().max() < 1e-5
    finally:
        if os.path.isfile(new_filename):
            os.remove(new_filename)


def test_event_selection_scalars():
    original_file = uproot.open('tests/scalars_tree_file.root')
    treename = 'tree'
    original_tree = original_file[treename]
    new_filename = tempfile.mkstemp(suffix='.root', dir=os.getcwd())[1]
    try:
        clone_tree(original_tree, new_filename, selection=[False, True])
        new_file = uproot.open(new_filename)
        new_tree = new_file[treename]
        assert new_tree['int_branch'].array().tolist() == [-1]
        assert new_tree['long_branch'].array().tolist() == [-2]
        assert np.allclose(new_tree['float_branch'].array(), [3.3])
        assert np.allclose(new_tree['double_branch'].array(), [4.4])
        assert new_tree['bool_branch'].array().tolist() == [True]
    finally:
        if os.path.isfile(new_filename):
            os.remove(new_filename)


def test_event_selection_vectors():
    original_file = uproot.open('tests/vectors_tree_file.root')
    treename = 'tree'
    original_tree = original_file[treename]
    new_filename = tempfile.mkstemp(suffix='.root', dir=os.getcwd())[1]
    try:
        clone_tree(original_tree, new_filename, selection=[True, False, True])
        new_file = uproot.open(new_filename)
        new_tree = new_file[treename]
        assert new_tree['int_vector_branch'].array().tolist() == [[], [13]]
        assert abs(new_tree['float_vector_branch'].array() - awkward.fromiter([[], [15.15]])).max().max() < 1e-5
        assert abs(new_tree['double_vector_branch'].array() - awkward.fromiter([[], [16.16]])).max().max() < 1e-5
    finally:
        if os.path.isfile(new_filename):
            os.remove(new_filename)


def test_new_scalar_branch():
    original_file = uproot.open('tests/scalars_tree_file.root')
    treename = 'tree'
    original_tree = original_file[treename]
    new_filename = tempfile.mkstemp(suffix='.root', dir=os.getcwd())[1]
    try:
        new_branch_dictionary = {'new_int_branch': np.array([5, 6])}
        clone_tree(original_tree, new_filename, new_branches=new_branch_dictionary)
        new_file = uproot.open(new_filename)
        new_tree = new_file[treename]
        assert new_tree['int_branch'].array().tolist() == [0, -1]
        assert new_tree['long_branch'].array().tolist() == [0, -2]
        assert np.allclose(new_tree['float_branch'].array(), [0.0, 3.3])
        assert np.allclose(new_tree['double_branch'].array(), [0.0, 4.4])
        assert new_tree['bool_branch'].array().tolist() == [False, True]
        assert new_tree['new_int_branch'].array().tolist() == [5, 6]
    finally:
        if os.path.isfile(new_filename):
            os.remove(new_filename)


def test_new_vector_branch():
    original_file = uproot.open('tests/vectors_tree_file.root')
    treename = 'tree'
    original_tree = original_file[treename]
    new_filename = tempfile.mkstemp(suffix='.root', dir=os.getcwd())[1]
    try:
        new_branch_dictionary = {'new_int_vector_branch': awkward.fromiter([[1], [2, 3], []])}
        clone_tree(original_tree, new_filename, new_branches=new_branch_dictionary)
        new_file = uproot.open(new_filename)
        new_tree = new_file[treename]
        assert new_tree['int_vector_branch'].array().tolist() == [[], [-1, 2, 3], [13]]
        assert abs(new_tree['float_vector_branch'].array() - awkward.fromiter([[], [-7.7, 8.8, 9.9], [15.15]])).max().max() < 1e-5
        assert abs(new_tree['double_vector_branch'].array() - awkward.fromiter([[], [-10.10, 11.11, 12.12], [16.16]])).max().max() < 1e-5
        assert new_tree['new_int_vector_branch'].array().tolist() == [[1], [2, 3], []]
    finally:
        if os.path.isfile(new_filename):
            os.remove(new_filename)


def test_select_branches():
    original_file = uproot.open('tests/scalars_tree_file.root')
    treename = 'tree'
    original_tree = original_file[treename]
    new_filename = tempfile.mkstemp(suffix='.root', dir=os.getcwd())[1]
    try:
        branch_list = ['float_branch', 'bool_branch']
        clone_tree(original_tree, new_filename, branches=branch_list)
        new_file = uproot.open(new_filename)
        new_tree = new_file[treename]
        assert set(map(lambda b: b.decode('utf-8'), new_tree.keys())) == set(branch_list)
        assert np.allclose(new_tree['float_branch'].array(), [0.0, 3.3])
        assert new_tree['bool_branch'].array().tolist() == [False, True]
    finally:
        if os.path.isfile(new_filename):
            os.remove(new_filename)
