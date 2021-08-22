Git fork/PR workflow
--------------------
This repository uses the [forking model](https://www.atlassian.com/git/tutorials/comparing-workflows/forking-workflow)
for collaboration. In this model,
each developer forks the main (indralab/pybiopax) repository, pushes code
only to branches in their own fork, and then submits pull requests to
`indralab`. After cloning your own fork of `pybiopax`, you should add `indralab`
as a remote to be able to track the latest changes by doing

```
git remote add indralab git@github.com:indralab/pybiopax.git
```

When a PR is submitted from a branch, any further changes can be pushed
to that same branch even after the PR has been opened; those changes
are automatically appended to the PR. Please always check the box on Github
allowing the maintainers of the repo to make changes to the PR.

In addition, as a convention, we only merge PRs whose branches are rebased
on top of the latest indralab/master. This means that instead of merging
indralab/master into your own branch to resolve conflicts, you should always
rebase on top of indralab/master and force push your branches if
needed (you can do this even if a PR from that branch is already open).
Consistent with this convention, in general, you should not use `git pull`
to update your local fork. Rather, use `git fetch --all`,
`git merge --ff-only`, `git rebase` or `git reset --hard` as needed to
get to the desired state. PRs are always merged using a separate merge commit,
ensuring that merges clearly correspond to the inclusion of a specific
feature or the fixing of a specific issue. In some cases, for instance, if
a branch includes many trial and error commits, the maintainers may squash
some commits before merging.

Pull requests
-------------
Always submit PRs via the indralab repository.
Give your PR a concise and clear title that describes without excessive detail
what the PR does. You should give more details in the description, pointing
out the important changes made and any additional remarks that are relevant.
If the PR fixes any issues, you can add "Fixes #xxx" to the text of the PR,
which, when merged, will also automatically close the issue.
The branch itself should have a short but recognizable name related to the
feature it adds or fixes rather than a generic name (e.g. patch, fix).

Commit messages
---------------
The commit message should typically consist of a single line describing what
the commit does. A good commit is one for which a clear and concise commit
message is necessary and sufficient - irrespective of how much code the commit
changes. A good set of guidelines can be found
[here](https://chris.beams.io/posts/git-commit/).

Code style
----------
Please follow [PEP8 guidelines](https://www.python.org/dev/peps/pep-0008/)
when implementing new code. If modifying existing
code, we ask that you do not mix extensive stylistic changes with meaningful
code changes. Any stylistic changes should be submitted in a separate PR.

The most important stylistic requirements are:
- use 4 spaces for indentation instead of tabs
- wrap lines to max 80 characters
- name variables and functions all lowercase with underscore as a separator
(e.g. `some_variable`)
- name classes with starting letters capitalized and no separator
(e.g. `SomeClass`)

In addition, functions or classes that are not meant to be part of the API
of the given module (for instance helper functions that a user wouldn't
directly call) should be prefixed with an underscore. These then won't show
up and clutter the auto-generated API documentation.

Python version compatibility
----------------------------
PyBioPAX is compatible with Python versions 3.6 and later. Therefore, features
only available in Python versions later than 3.6 should not be used.

Documentation
-------------
All API functions (i.e. functions that a user can call) and classes need to be
documented via docstrings. Please follow the
[NumPy documentation style](https://numpydoc.readthedocs.io/en/latest/format.html)
when adding docstrings to functions and classes.

The docstring
- is surrounded by triple double-quotes,
- starts with a one line short summary on the same line as the starting quotes,
- after the short summary and an empty line, can contain an arbitrary length
extended summary,
- lists all arguments, their types and descriptions in a Parameters block
- lists all returned values, their types and descriptions in a Returns block

To verify that the documentation build is working, go into the `doc` folder
and run `make html`. Warnings and errors indicate any issues during the build
process. The resulting HTML documentation can be opened with a browser from
`doc/_build/html/index.html` and inspected to verify that it looks as
intended.

Testing
-------
PyBioPAX is tested using the `nosetests` package.
See the [nose documentation](http://nose.readthedocs.io/en/latest/) for more
details.

All new functionalities added should also be tested. Similarly, fixed bugs
should have regression tests added. Normally, any test file with `test` in its
name and any functions/classes that have `test/Test` in their names in these
files will be automatically discovered and tested. Tests should generally be
included in `pybiopax/tests`, and new tests should be placed in the appropriate
existing file, if possible. Otherwise, add a new file using the
`test_<module_name>.py` naming convention. Where possible, tests should be
short and focused. If the newly added test requires special dependencies or
other preliminary setup, the `.github/workflows/tests.yml` configuration for
GitHub Actions needs to be updated to make the test work. PRs will not be
merged unless tests are passing.

Logging
-------
Instead of using `print` for printing information to stdout, use the `logging`
module to first create an approproately named logger,
as for instance `logger = logging.getLogger(__name__)` and then use the
appropriate level of logging (typically debug, info, warning or error) with
the logger object to print messages. The configuration of the logging format
is uniform across PyBioPAX without further configuration needed for each
individual logger instance. In addition, by using `__name__` to instantiate
the logger, the hierarchy of logger objects across the module is maintained
making it easier to control logging at various levels.

New dependencies
----------------
When adding new features, using built-in Python libraries or
packages that are already standard dependencies of PyBioPAX is strongly
preferred.  In case a new dependency needs to be used, that dependency needs to
be
- added to the install list or one of the extras list in setup.py
- added to the installation instructions in the documentation if any special
  instructions are needed for setup
- added to doc/requirements.txt as an installed dependency
- added to .github/workflows/tests.yml unless installed via setup.py
