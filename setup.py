import re
from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as fh:
    long_description = fh.read()

with open(path.join(here, 'pybiopax', '__init__.py'), 'r') as fh:
    for line in fh.readlines():
        match = re.match(r'__version__ = \'(.+)\'', line)
        if match:
            version = match.groups()[0]
            break
    else:
        raise ValueError('Could not get version from pybiopax/__init__.py')


setup(name='pybiopax',
      version=version,
      description=('A Python implementation of the BioPAX object model, '
                   'and parts of PaxTools.'),
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/indralab/pybiopax',
      author='Benjamin M. Gyori, Harvard Medical School',
      author_email='benjamin_gyori@hms.harvard.edu',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'License :: OSI Approved :: BSD License',
      ],
      packages=find_packages(),
      install_requires=['lxml', 'requests', 'tqdm'],
      tests_require=['pytest', 'pytest-cov', 'tox'],
      keywords=['biology', 'pathway']
      )
