import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='uproot_tree_utils',
                 version=0.2,
                 description='A small collection of utilities for handling ROOT TTrees with uproot.',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 packages=setuptools.find_packages(exclude=['tests']),
                 install_requires=['numpy', 'uproot'],
                 author='Mason Proffitt',
                 author_email='masonlp@uw.edu',
                 url='https://github.com/masonproffitt/uproot_tree_utils')
