import numpy as np

import uproot


def clone_tree(tree, new_filename, new_treename=None, branches=None, selection=None, new_branches=None):
    if new_treename is None:
        new_treename = tree.name.decode('utf-8')
    if branches is None:
        branchnames = list(map(lambda b: b.decode('utf-8'), tree.keys()))
    else:
        branchnames = branches
    branch_definition_dictionary = dict()
    branch_content_dictionary = dict()
    for name in branchnames:
        branch = tree[name]
        if isinstance(branch.interpretation.type, np.dtype):
            branch_definition_dictionary[name] = uproot.newbranch(branch.interpretation.type)
        elif isinstance(branch.interpretation.content.type, np.dtype):
            if branch.interpretation.content.type == np.dtype('int64'):
                raise NotImplementedError('Jagged arrays of 64-bit integers are not yet supported'
                                          ' due to a known bug in the tree-writing code'
                                          ' (https://github.com/scikit-hep/uproot/issues/506).')
            size_name = name + '_n'
            while size_name in branchnames:
                size_name += '0'
            branch_definition_dictionary[name] = uproot.newbranch(branch.interpretation.content.type, size=size_name)
            if selection is not None:
                branch_content_dictionary[size_name] = branch.array().count()[selection]
            else:
                branch_content_dictionary[size_name] = branch.array().count()
        else:
            raise NotImplementedError('Branch type (' + str(branch.interpretation) + ') not supported')
        if selection is not None:
            content = branch.array()[selection]
        else:
            content = branch.array()
        branch_content_dictionary[name] = content
    if new_branches is not None:
        for name, content in new_branches.items():
            if isinstance(content, np.ndarray) and len(content.shape) == 1:
                branch_definition_dictionary[name] = uproot.newbranch(content.dtype)
            elif isinstance(content.content, np.ndarray):
                if branch.interpretation.content.type == np.dtype('int64'):
                    raise NotImplementedError('Jagged arrays of 64-bit integers are not yet'
                                              ' supported due to a known bug in the tree-writing'
                                              ' code'
                                              ' (https://github.com/scikit-hep/uproot/issues/506)'
                                              '.')
                size_name = name + '_n'
                while size_name in branchnames + list(new_branches.keys()):
                    size_name += '0'
                branch_definition_dictionary[name] = uproot.newbranch(content.content.dtype, size=size_name)
                branch_content_dictionary[size_name] = content.count()
            else:
                raise NotImplementedError('Branch type (' + str(type(content)) + ') not supported')
            branch_content_dictionary[name] = content
    with uproot.recreate(new_filename) as new_file:
        new_file[new_treename] = uproot.newtree(branch_definition_dictionary)
        new_file[new_treename].extend(branch_content_dictionary)
