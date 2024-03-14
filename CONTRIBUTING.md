# Contributing

## Prerequisites

### Poetry
Install `poetry`

```bash
pipx install poetry
```

Learn more about poetry at https://python-poetry.org/

### Make

`make` is included with xcode. If you don't already have it install it:
```bash
xcode-select --install
```

## Development for JupyterLab

1. run a local JupyterLab instance:
    ```bash
    make jupyterlab-dev
    ```

    then go to http://localhost:8888

1. make changes to the `skillsnetwork` package
1. restart your kernel
1. test your changes

## Development for JupyterLite

1. run a local pypi instance:
    ```bash
    make local-pypi
    ```

1. run a local JupyterLite instance:
    ```bash
    make jupyterlite-dev
    ```

    then go to http://localhost:8000


1. install the package in JupyterLite (note: your version may be different. You can go to http://localhost:3000/skillsnetwork to see available versions):
    ```python
    import piplite
    await piplite.install("http://localhost:3000/skillsnetwork/skillsnetwork-0.0.0-py3-none-any.whl")
    ```

1. make changes to the `skillsnetwork` package
1. stop the local pypi server with Ctrl+c, then re-start it with `make local-pypi`
1. restart your kernel
1. reinstall the package to get the latest changes
1. test your changes

## Publishing

To publish a new version of the package on PyPI, create a new GitHub release. Pre-releasese are supported and will also be published to PyPI (as pre-releases).
