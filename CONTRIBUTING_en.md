# How to contribute
## Prerequisite
Install poetry. This tool resolves dependencies, build the package, and publish it.

Installation in Linux and macOS:
```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

In Windows, use PowerShell:
```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
```

Detailed instruction: [poetry documentation](https://python-poetry.org/docs/#installation)

## Using poetry
We introduce basic usage of poetry here.
For further information, refer to [Basic usage](https://python-poetry.org/docs/basic-usage) and [Commands](https://python-poetry.org/docs/cli/).

### Virtual environment
poetry creates a virtual environment to manage dependencies.
When you use VSCode, it is useful to create it under the root of the project.
First, change configuration.
```bash
poetry config virtualenvs.in-project true
```

### Dependency management
poetry manages list of dependencies in `pyproject.toml`.
To add a new dependency to the file, run
```bash
poetry add numpy
```

If you want to install a package only for development, add `-D` flag.
```bash
poetry add -D black
```

And install dependencies
```bash
poetry install
```
This command updates `poetry.lock`. Any developer can install exact same version of dependencies with this file, so be sure to commit this file.

You can update dependencies to latest versions with following command.
```bash
poetry update
```

### Run scripts and commands
You can run scripts and commands in the virtual environment.
```bash
poetry run python main.py
poetry run python
```

In other words, you cannot use packages you installed in the virtual environment if you just run `python main.py`.

When you run in VSCode, select `./.venv/bin/python`(`./.venv/Scripts/python.exe` in Windows) as Python interpreter of the project.
You can refer to [Using Python environments in VS Code](https://code.visualstudio.com/docs/python/environments#_select-and-activate-an-environment) to see how to configure it.

### Build and publish
To build the project to wheel archive, just run:
```bash
poetry build
```

For publish the package, refer to [How to Publish a Python Package to PyPI using Poetry](https://towardsdatascience.com/how-to-publish-a-python-package-to-pypi-using-poetry-aa804533fc6f).

## Start coding
1. Clone this repository.
2. Synchronize with `main` branch.
```bash
git switch main
git pull
```

3. Create branch with name describing a feature you are going to develop. Branch name format is `${ISSUE_NUMBER}-${FEATURE}`
```bash
git switch -c 99-wonderful-model
```

4. Install dependencies. This is not needed when there is no dependency installed recently.
```bash
poetry install
```

5. Then write your code. If you create a new file, add it to git index for following steps.
```bash
git add NEW_FILE
```

6. Format, lint, and test your code.
```bash
make check
make test
```

There might remain some errors. They cannot be fixed automatically, so fix them manually.

7. After coding, commit and push changes.
```bash
git add -p
git commit
# For the first push in the branch
git push -u origin 99-wonderful-model
# After first push
git push
```

8. Create a pull request(PR) after you finish the development at the branch. Basically you need someone to review your code. After reviewer approved and all CI passed, merge the branch to `main`.

## Testing
Write tests when you develop a new feature. Tests are executed automatically.

1. Create `test_*.py` in `tests` directory. Describe what to test in the file name.
2. Create a function whose name starts with `test_`. Write assertion to check if a function you developed is compliant with a specification. For example, a test for a function calculating sum of two integers is like following.
```python
from your_module import add
def test_add():
    assert 3 == add(1, 2)
```

3. Then run tests.
```bash
make test
```
If the assertion fails, error contents are displayed with red. If you do not see that, all test are successful.

You might want to run tests only in specific files.
In that case, run `make` with file(s) you want to test.
```bash
make tests/test_sample.py
```

We use `pytest` for testing. Detailed instructions are available in the [document](https://docs.pytest.org/en/6.2.x/).

## Handle linter error
Most linter errors must be fixed, but you may encounter some linter errors which you cannot fix.
In this case, you can ignore the error by adding some comments.

For example, if you check this code with linter,
```python
example = lambda: "example"
```

you will got an error something like this:
```
E731 do not assign a lambda expression, use a def
```

`E731` is error code and following text is the contents of the error.
You can ignore this error by adding `# noqa E731` at the end of line.
```python
example = lambda: "example"  # noqa E731
```

Any linter error code is acceptable instead of `E731`.
You can find more information at [flake8 document](https://flake8.pycqa.org/en/3.1.1/user/ignoring-errors.html#in-line-ignoring-errors).

This method is a kind of workaround.
You should discuss on a PR review whether this approach is adopted.

## CI
Run CI at GitHub Actions. You should not merge a branch unless CI passes.
In CI, we run tests and check code format and linter error.
The purpose of CI is
* Share our code works properly in the team.
* Find error you cannot notice at your local machine.
* Avoid unnecessary diff by forcing code format and linter error.

## Documentation
You can publish the repository's documentation at [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/about-github-pages). It can include Jupyter Notebook format tutorial and API documentation generated from comments in the source code. HTML files for the Web site is generated automatically from these contents.

### Tutorial by Jupyter Notebook
You can create tutorial pages from Jupyter Notebook.

1. Create file like `1.1_wonderful_tutorial.ipynb` in `doc/source/notebooks`. 1 file corresponds to 1 page in the Web site.
2. Add title like `# Wonderful Tutorial` in the first Markdown cell. This is displayed at index page of the document as a title.
3. Add contents.
4. Add a line `1.1_wonderful_tutorial`(file name without its extension) to `doc/source/notebooks/index.rst` like this:
```
.. toctree::

   1.1_wonderful_tutorial
```

Images used in notebooks should be stored at `doc/source/notebooks/figs`. It is recommended to name the images with the section number: e.g. `1.1_wonderful_graph.png`.

Detailed instructions of Markdown and code cells are available: [An example Jupyter Notebook](https://myst-nb.readthedocs.io/en/latest/examples/basic.html)

### API Documentation
API documentation is generated from documentation comments(docstring) which are put just after a definition of function or class. This is an example:
```python
def wonderful_func(x: Int, y: str) -> str:
    """Summary line(one line is preferred).

    Detailed description.
    You can use multiple lines.

    Args:
        x: Description of argument x.
        y: Description of argument y.

    Examples:
    >>> a = add(2, 3)

    Returns:
        Description of return value.
    """
    return x + y
```

For more detail, refer to [Sphinx document](https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html).

### Build
To build the documentation as HTML files, just run following:
```bash
make html
```

Then HTML files are generated under `doc/build/html`. You can open them in your browser.
Or you can build and serve them at localhost by just running this command:
```bash
make serve  # Serves at http://localhost:8000
make serve PORT=12345  # Or you can serve at other port.
```

### Publish
When PR is merged into `main` branch, the documentation is automatically generated and published to GitHub Pages. Generated HTML files are pushed to `gh-pages` branch, so do not edit and delete the branch.
