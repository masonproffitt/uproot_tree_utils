import numpy as np

import uproot


def clone_tree(tree, new_file_name, new_tree_name=None):
    if new_tree_name is None:
        new_tree_name = tree.name.decode('utf-8')
    branch_definition_dictionary = dict()
    branch_content_dictionary = dict()
    for branch in tree.values():
        name = branch.name.decode('utf-8')
        if isinstance(branch.interpretation.type, np.dtype):
            branch_definition_dictionary[name] = uproot.newbranch(branch.interpretation.type)
            branch_content_dictionary[name] = branch.array()
        elif isinstance(branch.interpretation.content.type, np.dtype):
            size_name = name + '_n'
            while bytes(size_name, 'utf-8') in tree.keys():
                size_name += '0'
            branch_definition_dictionary[name] = uproot.newbranch(branch.interpretation.content.type, size=size_name)
            branch_content_dictionary[name] = branch.array()
            branch_content_dictionary[size_name] = branch.array().count()
        else:
            raise NotImplementedError('Branch type (' + str(branch.interpretation) + ') not supported')
    with uproot.recreate(new_file_name) as new_file:
        new_file[new_tree_name] = uproot.newtree(branch_definition_dictionary)
        new_file[new_tree_name].extend(branch_content_dictionary)
