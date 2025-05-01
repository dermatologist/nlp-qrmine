conda install conda-forge::uv
uv pip install ini2toml
ini2toml setup.cfg -o pyproject.toml

delete setup.cpg
delete requirements.txt, dev-requirements.txt, dev-requirements.in
remove deps from tox.ini

uv pip install -e .
see pr.yml for GitHub actions
see pyproject.toml for pytorch cpu install
uv pip install -e .

uv sync --all-extras --dev
uv pip install pip
uv run python -m spacy download en_core_web_sm

pyproject.toml
requires = ["setuptools>=61.2", "wheel", "pip"]

dev = [
    "setuptools",
    "setuptools_scm",
    "pytest",
    "pytest-cov",
    "tox",
    "black",
    "recommonmark",
    "sphinx",
    "wheel",
    "twine",
    "tox",
]

