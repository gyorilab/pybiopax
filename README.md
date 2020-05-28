PyBioPAX: A python implementation of the BioPAX object model
------------------------------------------------------------

PyBioPAX implements the BioPAX level 3 object model (
http://www.biopax.org/release/biopax-level3-documentation.pdf) as a set of
Python classes. It exposes API functions to read OWL files into this
object model, and to dump OWL files from this object model.
This allows for the processing and creation of BioPAX models natively in
Python.

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

Each BioPaxObject has attributes that are consistent with the
BioPAX level 3 specification.


Funding
-------
The development of PyBioPAX is funded under the DARPA Communicating with
Computers program (ARO grant W911NF-15-1-0544).
