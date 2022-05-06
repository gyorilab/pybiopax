PyBioPAX: A python implementation of the BioPAX object model
------------------------------------------------------------
[![License](https://img.shields.io/badge/License-BSD%202--Clause-orange.svg)](https://opensource.org/licenses/BSD-2-Clause)
[![DOI](https://joss.theoj.org/papers/10.21105/joss.04136/status.svg)](https://doi.org/10.21105/joss.04136)
[![Build](https://github.com/indralab/pybiopax/workflows/Tests/badge.svg)](https://github.com/indralab/pybiopax/actions)
[![Documentation](https://readthedocs.org/projects/pybiopax/badge/?version=latest)](https://pybiopax.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/pybiopax.svg)](https://badge.fury.io/py/pybiopax)
[![Python 3](https://img.shields.io/pypi/pyversions/pybiopax.svg)](https://www.python.org/downloads/release/python-357/)

PyBioPAX implements the BioPAX level 3 object model (http://www.biopax.org/release/biopax-level3-documentation.pdf) as a set of
Python classes. It exposes API functions to read OWL files into this
object model, and to dump OWL files from this object model.
This allows for the processing and creation of BioPAX models natively in
Python.

Gyori BM, Hoyt CT (2022). PyBioPAX: biological pathway exchange in Python. Journal of Open Source Software, 7(71), 4136, [https://doi.org/10.21105/joss.04136](https://doi.org/10.21105/joss.04136)

Installation
------------
PyBioPAX can be installed from PyPI as a package:

```bash
$ pip install pybiopax
```

Usage
-----
Reading an OWL file into a BioPaxModel object:

```python
import pybiopax
model = pybiopax.model_from_owl_file('test.owl')
```


Writing a BioPaxModel into an OWL file:

```python
import pybiopax
pybiopax.model_to_owl_file(model, 'test.owl')
```

Querying Pathway Commons to get a BioPaxModel object:

```python
import pybiopax
model = pybiopax.model_from_pc_query('pathsfromto', ['MAP2K1'], ['MAPK1'])
```

Working with the elements of the Python object model:

```python
import pybiopax
model = pybiopax.model_from_pc_query('pathsfromto', ['MAP2K1'], ['MAPK1'])

# Each BioPaxModel instance has an objects attribute which is a dict
# whose keys are object URIs (strings) and values are BioPaxObject instances.
assert isinstance(model.objects, dict)
assert all(isinstance(obj, pybiopax.biopax.BioPaxObject)
           for obj in model.objects.values())

# Let's look at a specific object
bcr = model.objects['BiochemicalReaction_4f689747397d98089c551022a3ae2d88']

# This is a BiochemicalReaction which has a left and a right side. All list/set
# types per the BioPAX specification are represented as lists in the Python
# object model
# Both left and right consist of a single protein
left = bcr.left[0]
assert isinstance(left, pybiopax.biopax.Protein)
assert left.display_name == 'ERK1-2'
right = bcr.right[0]
assert isinstance(right, pybiopax.biopax.Protein)
assert right.display_name == 'ERK1-2-active'
```

We can also use the `pybiopax.paths` module to construct iterators over
objects based on a string specification from a given starting point.
Continuing from the block of code above, we take the BiochemicalReaction
`bcr` and link to reactants on its left hand side, then linking to their
entity references, and finally linking back to all the physical entities
that those are references of.

```python
from pybiopax.paths import find_objects

erks = find_objects(bcr, 'left/entity_reference/entity_reference_of')
```

Contribution and support
------------------------
To contribute to the code, please submit a pull request after
reading the [contribution guidelines](https://github.com/indralab/pybiopax/blob/master/CONTRIBUTING.md).
To report bugs and issues, or ask questions related to PyBioPAX, please
submit an [issue](https://github.com/indralab/pybiopax/issues).

Funding
-------
Development of this software was supported by the Defense Advanced Research
Projects Agency under award W911NF-15-1-0544 and the National Cancer Institute
under award U54-CA225088.
