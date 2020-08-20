# uproot_tree_utils

[![codecov](https://codecov.io/gh/masonproffitt/uproot_tree_utils/branch/master/graph/badge.svg)](https://codecov.io/gh/masonproffitt/uproot_tree_utils)

A small collection of utilities for handling ROOT TTrees with uproot.

## Usage

The only function currently in the package is `clone_tree()`. The full function signature is

```python
clone_tree(tree, new_filename, new_treename=None, branches=None, selection=None, new_branches=None)
```

The required arguments `tree` and `new_filename` are the TTree object to copy from (as retrieved by uproot) and the file to copy to, respectively. The simplest usage looks like

```python
import uproot
from uproot_tree_utils import clone_tree

file = uproot.open('some_root_file.root')
clone_tree(file['the_treename'], 'a_new_filename.root')
```

This will simply copy the entire tree from the original file to a new file (with no other objects).

- `new_treename` can be used to give the new tree a different name. The default is the original tree's name.
- `branches` can be a list of strings representing the branches to copy. Only the selected branches will be in the new file.
- `selection` is an optional array determining which events to copy. This can be a boolean mask or integers corresponding to the desired event indices.
- `new_branches` allows the user to pass a dictionary of new branches to insert into the tree. The format for the dictionary should be `{'new_branchname': array_with_branch_data}`.

## Limitations

Not all branch types can be written by uproot.

Currently supported branch types:

- `Char_t`/`char`
- `Short_t`/`short`
- `Int_t`/`int`
- `Float_t`/`float`
- `Double_t`/`double`
- `Long64_t`/`long long`
- `Bool_t`/`bool`
- `std::vector<short>`
- `std::vector<int>`
- `std::vector<float>`
- `std::vector<double>`

Character strings, unsigned integers, `vector<char>`, and `vector<bool>` are not yet supported. There are also some known bugs with `vector<long>` and `vector<long long>`. Further nesting of vectors (e.g. `vector<vector<int> >`) is not supported by uproot's tree writing.
