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

```
pip install pybiopax
```

Usage
-----
Reading an OWL file into a BioPaxModel object:

```
from pybiopax import model_from_owl_file
model = model_from_owl_file('test.owl')
```


Writing a BioPaxModel into an OWL file:

```
from pybiopax import model_to_owl_file
model_to_owl_file(model, 'test.owl')
```

Working with the elements of the Python object model:

```
from pybiopax.biopax import *
# Each BioPaxModel instance has an objects attribute which is a dict
# whose keys are object URIs (strings) and values are BioPaxObject instances.
assert isinstance(model.objects, dict)
assert all(isinstance(obj, BioPaxObject) for obj in model.objects.values())
```

Each BioPaxObject has attributes that are consistent with the
BioPAX level 3 specification.


Funding
-------
The development of PyBioPAX is funded under the DARPA Communicating with
Computers program (ARO grant W911NF-15-1-0544).
