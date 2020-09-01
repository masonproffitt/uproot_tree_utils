import numpy as np

import uproot


def write_tree(branches, filename, treename):
    """
    Write a TTree to a new ROOT file from a collection of arrays.

    Parameters
    ----------
    branches : dict
        Dictionary of `branchname: branch_data` pairs.
    filename : str
        Pathname of new ROOT file.
    treename : str
        Name of new TTree.
    """
    branch_definition_dictionary = dict()
    branch_content_dictionary = dict()
    for name, content in branches.items():
        if isinstance(content, np.ndarray) and len(content.shape) == 1:
            branch_definition_dictionary[name] = uproot.newbranch(content.dtype)
        elif isinstance(content.content, np.ndarray):
            if content.content.dtype == np.dtype('int64'):
                raise NotImplementedError('Jagged arrays of 64-bit integers are not yet'
                                          ' supported due to a known bug in the tree-writing'
                                          ' code'
                                          ' (https://github.com/scikit-hep/uproot/issues/506)'
                                          '.')
            size_name = name + '_n'
            branch_definition_dictionary[name] = uproot.newbranch(content.content.dtype, size=size_name)
            branch_content_dictionary[size_name] = content.count()
        else:
            raise NotImplementedError('Branch type (' + str(type(content)) + ') not supported')
        branch_content_dictionary[name] = content
    with uproot.recreate(filename) as file:
        file[treename] = uproot.newtree(branch_definition_dictionary)
        file[treename].extend(branch_content_dictionary)
