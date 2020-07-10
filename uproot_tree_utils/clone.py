import numpy as np

import uproot


def clone_tree(tree, new_file_name, new_tree_name=None, selection=None, new_branches=None):
    if new_tree_name is None:
        new_tree_name = tree.name.decode('utf-8')
    branch_definition_dictionary = dict()
    branch_content_dictionary = dict()
    for branch in tree.values():
        name = branch.name.decode('utf-8')
        if isinstance(branch.interpretation.type, np.dtype):
            branch_definition_dictionary[name] = uproot.newbranch(branch.interpretation.type)
        elif isinstance(branch.interpretation.content.type, np.dtype):
            size_name = name + '_n'
            while bytes(size_name, 'utf-8') in tree.keys():
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
                size_name = name + '_n'
                while bytes(size_name, 'utf-8') in tree.keys() or size_name in new_branches.keys():
                    size_name += '0'
                branch_definition_dictionary[name] = uproot.newbranch(content.content.dtype, size=size_name)
                branch_content_dictionary[size_name] = content.count()
            else:
                raise NotImplementedError('Branch type (' + str(type(content)) + ') not supported')
            branch_content_dictionary[name] = content
    with uproot.recreate(new_file_name) as new_file:
        new_file[new_tree_name] = uproot.newtree(branch_definition_dictionary)
        new_file[new_tree_name].extend(branch_content_dictionary)
