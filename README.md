# uproot_tree_utils

A small collection of utilities for handling ROOT TTrees with uproot.

## Usage

The only function currently in the package is `clone_tree()`. The full function signature is

```python
clone_tree(tree, new_file_name, new_tree_name=None, branches=None, selection=None, new_branches=None)
```

The required arguments `tree` and `new_file_name` are the TTree object to copy from (as retrieved by uproot) and the file to copy to, respectively. The simplest usage looks like

```python
import uproot
from uproot_tree_utils import clone_tree

file = uproot.open('some_root_file.root')
clone_tree(file['the_tree_name'], 'a_new_file_name.root')
```

This will simply copy the entire tree from the original file to a new file (with no other objects).

`branches` can be a list of strings representing the branches to copy. Only the selected branches will be in the new file.

`selection` is an optional array determining which events to copy. This can be a boolean mask or integers corresponding to the desired event indices.

`new_branches` allows the user to pass a dictionary of new branches to insert into the tree. The format for each dictionary entry should be `{'new_branch_name': array_with_branch_data}`.

## Limitations

Not all branch types can be written by uproot. The types tested so far are `int`, `long`, `float`, `double`, `bool`, `vector<int>`, `vector<float>`, and `vector<double>`. Further nesting of vectors (e.g. `vector<vector<int> >` is not yet supported by uproot's tree writing. There are also some known bugs with `vector<long>` and `vector<bool>`. `string` and `vector<string>` should be possible but are a bit trickier and haven't been implemented in this utility package yet.
