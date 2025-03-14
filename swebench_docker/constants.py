# Copyright (c) Meta Platforms, Inc. and affiliates.
# Adapted from: https://github.com/aorwall/SWE-bench-docker/blob/main/swebench_docker/context_manager.py

from enum import Enum
from typing import Any, Collection, Dict, List, Sequence, Union

PYTHON_ENVIRONMENT_VERSIONS: Dict[str, str] = {
    "3.5": "3.5.10",
    "3.6": "3.6.15",
    "3.7": "3.7.17",
    "3.8": "3.8.19",
    "3.9": "3.9.19",
    "3.10": "3.10.14",
    "3.11": "3.11.9",
}

PYENV_REPOS: set[str] = {"django/django", "psf/requests", "scikit-learn/scikit-learn"}

MAP_VERSION_TO_INSTALL_SKLEARN: Dict[str, Dict[str, Any]] = {
    k: {
        "instance_image": True,
        "python": "3.6",
        "packages": "numpy==1.19.2 scipy==1.5.2 cython==0.29.7 pytest==4.5.0 pandas matplotlib==3.1.0 joblib threadpoolctl",
        "install": "pip install -v --no-build-isolation -e .",
        "arch_specific_packages": {
            "aarch64": "gxx_linux-aarch64 gcc_linux-aarch64 make",
        },
    }
    for k in ["0.20", "0.21", "0.22"]
}
MAP_VERSION_TO_INSTALL_SKLEARN.update(
    {
        k: {
            "instance_image": True,
            "python": "3.9",
            "pre_install": ["pip install setuptools wheel"],
            "packages": "numpy scipy cython pytest pandas matplotlib joblib threadpoolctl",
            "install": "pip install -v --no-use-pep517 --no-build-isolation -e .",
            "arch_specific_packages": {
                "aarch64": "gxx_linux-aarch64 gcc_linux-aarch64 make",
            },
        }
        for k in ["1.3", "1.4"]
    }
)

MAP_VERSION_TO_INSTALL_FLASK: Dict[str, Dict[str, Any]] = {
    "2.0": {
        "python": "3.9",
        "packages": "requirements.txt",
        "install": "pip install -e .",
        "pip_packages": [
            "Werkzeug==2.3.7",
            "Jinja2==3.0.1",
            "itsdangerous==2.1.2",
            "click==8.0.1",
            "MarkupSafe==2.1.3",
        ],
    },
    "2.1": {
        "python": "3.10",
        "packages": "requirements.txt",
        "install": "pip install -e .",
        "pip_packages": [
            "click==8.1.3",
            "itsdangerous==2.1.2",
            "Jinja2==3.1.2",
            "MarkupSafe==2.1.1",
            "Werkzeug==2.3.7",
        ],
    },
}
MAP_VERSION_TO_INSTALL_FLASK.update(
    {
        k: {
            "python": "3.11",
            "packages": "requirements.txt",
            "install": "pip install -e .",
            "pip_packages": [
                "click==8.1.3",
                "itsdangerous==2.1.2",
                "Jinja2==3.1.2",
                "MarkupSafe==2.1.1",
                "Werkzeug==2.3.7",
            ],
        }
        for k in ["2.2", "2.3"]
    }
)

MAP_VERSION_TO_INSTALL_DJANGO: Dict[str, Dict[str, Any]] = {
    k: {
        "python": "3.5",
        "packages": "requirements.txt",
        "install": "python -m pip install -e .",
    }
    for k in ["1.7", "1.8", "1.9", "1.10", "1.11", "2.0", "2.1", "2.2"]
}
MAP_VERSION_TO_INSTALL_DJANGO.update(
    {
        k: {"python": "3.5", "install": "python setup.py install"}
        for k in ["1.4", "1.5", "1.6"]
    }
)
MAP_VERSION_TO_INSTALL_DJANGO.update(
    {
        k: {
            "python": "3.6",
            "packages": "requirements.txt",
            "install": "python -m pip install -e .",
        }
        for k in ["3.0", "3.1", "3.2"]
    }
)
MAP_VERSION_TO_INSTALL_DJANGO.update(
    {
        k: {
            "python": "3.8",
            "packages": "requirements.txt",
            "install": "python -m pip install -e .",
        }
        for k in ["4.0"]
    }
)
MAP_VERSION_TO_INSTALL_DJANGO.update(
    {
        k: {
            "python": "3.9",
            "packages": "requirements.txt",
            "install": "python -m pip install -e .",
        }
        for k in ["4.1", "4.2"]
    }
)
MAP_VERSION_TO_INSTALL_DJANGO.update(
    {
        k: {
            "python": "3.11",
            "packages": "requirements.txt",
            "install": "python -m pip install -e .",
        }
        for k in ["5.0"]
    }
)
for k in ["2.2", "3.0", "3.1"]:
    MAP_VERSION_TO_INSTALL_DJANGO[k].update(
        {"env_vars_test": {"LANG": "en_US.UTF-8", "LC_ALL": "en_US.UTF-8"}}
    )

MAP_VERSION_TO_INSTALL_REQUESTS: Dict[str, Dict[str, Any]] = {
    k: {"python": "3.9", "packages": "pytest", "install": "python -m pip install ."}
    for k in ["0.7", "0.8", "0.9", "0.11", "0.13", "0.14", "1.1", "1.2", "2.0", "2.2"]
    + ["2.3", "2.4", "2.5", "2.7", "2.8", "2.9", "2.10", "2.11", "2.12", "2.17"]
    + ["2.18", "2.19", "2.22", "2.26", "2.25", "2.27", "3.0"]
}

MAP_VERSION_TO_INSTALL_SEABORN: Dict[str, Dict[str, Any]] = {
    k: {
        "python": "3.9",
        "install": "pip install -e .",
        "pip_packages": [
            "contourpy==1.1.0",
            "cycler==0.11.0",
            "fonttools==4.42.1",
            "importlib-resources==6.0.1",
            "kiwisolver==1.4.5",
            "matplotlib==3.7.2",
            "numpy==1.25.2",
            "packaging==23.1",
            "pandas==2.1.0",
            "pillow==10.0.0",
            "pyparsing==3.0.9",
            "pytest",
            "python-dateutil==2.8.2",
            "pytz==2023.3.post1",
            "scipy==1.11.2",
            "six==1.16.0",
            "tzdata==2023.1",
            "zipp==3.16.2",
        ],
    }
    for k in ["0.11"]
}
MAP_VERSION_TO_INSTALL_SEABORN.update(
    {
        k: {
            "python": "3.9",
            "install": "pip install -e .[dev]",
            "pip_packages": [
                "contourpy==1.1.0",
                "cycler==0.11.0",
                "fonttools==4.42.1",
                "importlib-resources==6.0.1",
                "kiwisolver==1.4.5",
                "matplotlib==3.7.2",
                "numpy==1.25.2",
                "packaging==23.1",
                "pandas==2.1.0",
                "pillow==10.0.0",
                "pyparsing==3.0.9",
                "python-dateutil==2.8.2",
                "pytz==2023.3.post1",
                "scipy==1.11.2",
                "six==1.16.0",
                "tzdata==2023.1",
                "zipp==3.16.2",
            ],
        }
        for k in ["0.12", "0.13"]
    }
)

MAP_VERSION_TO_INSTALL_PYTEST: Dict[str, Dict[str, Any]] = {
    k: {"python": "3.9", "install": "pip install -e ."}
    for k in [
        "4.4",
        "4.5",
        "4.6",
        "5.0",
        "5.1",
        "5.2",
        "5.3",
        "5.4",
        "6.0",
        "6.2",
        "6.3",
        "7.0",
        "7.1",
        "7.2",
        "7.4",
        "8.0",
    ]
}
MAP_VERSION_TO_INSTALL_PYTEST["4.4"]["pip_packages"] = [
    "atomicwrites==1.4.1",
    "attrs==23.1.0",
    "more-itertools==10.1.0",
    "pluggy==0.13.1",
    "py==1.11.0",
    "setuptools==68.0.0",
    "six==1.16.0",
]
MAP_VERSION_TO_INSTALL_PYTEST["4.5"]["pip_packages"] = [
    "atomicwrites==1.4.1",
    "attrs==23.1.0",
    "more-itertools==10.1.0",
    "pluggy==0.11.0",
    "py==1.11.0",
    "setuptools==68.0.0",
    "six==1.16.0",
    "wcwidth==0.2.6",
]
MAP_VERSION_TO_INSTALL_PYTEST["4.6"]["pip_packages"] = [
    "atomicwrites==1.4.1",
    "attrs==23.1.0",
    "more-itertools==10.1.0",
    "importlib-metadata==1.6.0",
    "packaging==23.1",
    "pluggy==0.13.1",
    "py==1.11.0",
    "six==1.16.0",
    "wcwidth==0.2.6",
]
for k in ["5.0", "5.1", "5.2"]:
    MAP_VERSION_TO_INSTALL_PYTEST[k]["pip_packages"] = [
        "atomicwrites==1.4.1",
        "attrs==23.1.0",
        "more-itertools==10.1.0",
        "packaging==23.1",
        "pluggy==0.13.1",
        "py==1.11.0",
        "wcwidth==0.2.6",
    ]
MAP_VERSION_TO_INSTALL_PYTEST["5.3"]["pip_packages"] = [
    "attrs==23.1.0",
    "more-itertools==10.1.0",
    "packaging==23.1",
    "pluggy==0.13.1",
    "py==1.11.0",
    "wcwidth==0.2.6",
]
MAP_VERSION_TO_INSTALL_PYTEST["5.4"]["pip_packages"] = [
    "py==1.11.0",
    "packaging==23.1",
    "attrs==23.1.0",
    "more-itertools==10.1.0",
    "pluggy==0.13.1",
    "wcwidth==0.2.6",
]
MAP_VERSION_TO_INSTALL_PYTEST["5.4"]["pre_test"] = ["pip install -e ."]
MAP_VERSION_TO_INSTALL_PYTEST["6.0"]["pip_packages"] = [
    "attrs==23.1.0",
    "iniconfig==2.0.0",
    "more-itertools==10.1.0",
    "packaging==23.1",
    "pluggy==0.13.1",
    "py==1.11.0",
    "toml==0.10.2",
]
for k in ["6.2", "6.3"]:
    MAP_VERSION_TO_INSTALL_PYTEST[k]["pip_packages"] = [
        "attrs==23.1.0",
        "iniconfig==2.0.0",
        "packaging==23.1",
        "pluggy==0.13.1",
        "py==1.11.0",
        "toml==0.10.2",
    ]
MAP_VERSION_TO_INSTALL_PYTEST["7.0"]["pip_packages"] = [
    "attrs==23.1.0",
    "iniconfig==2.0.0",
    "packaging==23.1",
    "pluggy==0.13.1",
    "py==1.11.0",
]
for k in ["7.1", "7.2"]:
    MAP_VERSION_TO_INSTALL_PYTEST[k]["pip_packages"] = [
        "attrs==23.1.0",
        "iniconfig==2.0.0",
        "packaging==23.1",
        "pluggy==0.13.1",
        "py==1.11.0",
        "tomli==2.0.1",
    ]
MAP_VERSION_TO_INSTALL_PYTEST["7.4"]["pip_packages"] = [
    "iniconfig==2.0.0",
    "packaging==23.1",
    "pluggy==1.3.0",
    "exceptiongroup==1.1.3",
    "tomli==2.0.1",
]
MAP_VERSION_TO_INSTALL_PYTEST["8.0"]["pip_packages"] = [
    "iniconfig==2.0.0",
    "packaging==23.1",
    "pluggy==1.3.0",
    "exceptiongroup==1.1.3",
    "tomli==2.0.1",
]

MAP_VERSION_TO_INSTALL_MATPLOTLIB: Dict[str, Dict[str, Any]] = {
    k: {
        "python": "3.11",
        "packages": "environment.yml",
        "install": "python -m pip install -e .",
        "pip_packages": [
            "contourpy==1.1.0",
            "cycler==0.11.0",
            "fonttools==4.42.1",
            "kiwisolver==1.4.5",
            "numpy==1.25.2",
            "packaging==23.1",
            "pillow==10.0.0",
            "pyparsing==3.0.9",
            "python-dateutil==2.8.2",
            "six==1.16.0",
            "setuptools==66.1.1",
            "setuptools-scm==7.1.0",
            "typing-extensions==4.7.1",
        ],
        "arch_specific_packages": {
            "aarch64": "gxx_linux-aarch64 gcc_linux-aarch64 make",
        },
    }
    for k in ["3.5", "3.6", "3.7"]
}

MAP_VERSION_TO_INSTALL_MATPLOTLIB.update(
    {
        k: {
            "python": "3.8",
            "packages": "requirements.txt",
            "install": "python -m pip install -e .",
            "pip_packages": [],
            "arch_specific_packages": {
                "aarch64": "gxx_linux-aarch64 gcc_linux-aarch64 make",
            },
        }
        for k in ["3.1", "3.2", "3.3", "3.4"]
    }
)
MAP_VERSION_TO_INSTALL_MATPLOTLIB.update(
    {
        k: {
            "python": "3.7",
            "packages": "requirements.txt",
            "install": "python -m pip install -e .",
            "pip_packages": ["freetype"],
            "arch_specific_packages": {
                "aarch64": "gxx_linux-aarch64 gcc_linux-aarch64 make",
            },
        }
        for k in ["3.0"]
    }
)
MAP_VERSION_TO_INSTALL_MATPLOTLIB.update(
    {
        k: {
            "python": "3.5",
            "install": "python setup.py build; python setup.py install",
            "arch_specific_packages": {
                "aarch64": "gxx_linux-aarch64 gcc_linux-aarch64 make",
            },
        }
        for k in ["2.0", "2.1", "2.2", "1.0", "1.1", "1.2", "1.3", "1.4", "1.5"]
    }
)

MAP_VERSION_TO_INSTALL_SPHINX: Dict[str, Dict[str, Any]] = {
    k: {
        "python": "3.9",
        "pip_packages": ["tox"],
        "install": "pip install -e .[test]",
        "pre_install": ["sed -i 's/pytest/pytest -rA/' tox.ini"],
        "arch_specific_packages": {
            "aarch64": "gxx_linux-aarch64 gcc_linux-aarch64 make",
            "x86_64": "gxx_linux-64 gcc_linux-64 make",
        },
    }
    for k in ["1.5", "1.6", "1.7", "1.8", "2.0", "2.1", "2.2", "2.3", "2.4", "3.0"]
    + ["3.1", "3.2", "3.3", "3.4", "3.5", "4.0", "4.1", "4.2", "4.3", "4.4"]
    + ["4.5", "5.0", "5.1", "5.2", "5.3", "6.0", "6.2", "7.0", "7.1", "7.2"]
}
for k in ["3.0", "3.1", "3.2", "3.3", "3.4", "3.5", "4.0", "4.1", "4.2", "4.3", "4.4"]:
    MAP_VERSION_TO_INSTALL_SPHINX[k]["pre_install"].extend(
        [
            "sed -i 's/Jinja2>=2.3/Jinja2<3.0/' setup.py",
            "sed -i 's/sphinxcontrib-applehelp/sphinxcontrib-applehelp<=1.0.7/' setup.py",
            "sed -i 's/sphinxcontrib-devhelp/sphinxcontrib-devhelp<=1.0.5/' setup.py",
            "sed -i 's/sphinxcontrib-qthelp/sphinxcontrib-qthelp<=1.0.6/' setup.py",
            "sed -i 's/alabaster>=0.7,<0.8/alabaster>=0.7,<0.7.12/' setup.py",
            "sed -i \"s/'packaging',/'packaging', 'markupsafe<=2.0.1',/\" setup.py",
        ]
    )
    if k in ["4.2", "4.3", "4.4"]:
        MAP_VERSION_TO_INSTALL_SPHINX[k]["pre_install"].extend(
            [
                "sed -i 's/sphinxcontrib-htmlhelp>=2.0.0/sphinxcontrib-htmlhelp>=2.0.0,<=2.0.4/' setup.py",
                "sed -i 's/sphinxcontrib-serializinghtml>=1.1.5/sphinxcontrib-serializinghtml>=1.1.5,<=1.1.9/' setup.py",
            ]
        )
    elif k == "4.1":
        MAP_VERSION_TO_INSTALL_SPHINX[k]["pre_install"].extend(
            [
                (
                    "grep -q 'sphinxcontrib-htmlhelp>=2.0.0' setup.py && "
                    "sed -i 's/sphinxcontrib-htmlhelp>=2.0.0/sphinxcontrib-htmlhelp>=2.0.0,<=2.0.4/' setup.py || "
                    "sed -i 's/sphinxcontrib-htmlhelp/sphinxcontrib-htmlhelp<=2.0.4/' setup.py"
                ),
                (
                    "grep -q 'sphinxcontrib-serializinghtml>=1.1.5' setup.py && "
                    "sed -i 's/sphinxcontrib-serializinghtml>=1.1.5/sphinxcontrib-serializinghtml>=1.1.5,<=1.1.9/' setup.py || "
                    "sed -i 's/sphinxcontrib-serializinghtml/sphinxcontrib-serializinghtml<=1.1.9/' setup.py"
                ),
            ]
        )
    else:
        MAP_VERSION_TO_INSTALL_SPHINX[k]["pre_install"].extend(
            [
                "sed -i 's/sphinxcontrib-htmlhelp/sphinxcontrib-htmlhelp<=2.0.4/' setup.py",
                "sed -i 's/sphinxcontrib-serializinghtml/sphinxcontrib-serializinghtml<=1.1.9/' setup.py",
            ]
        )

for spec in MAP_VERSION_TO_INSTALL_SPHINX.values():
    spec["pre_test"] = spec["pre_install"]

MAP_VERSION_TO_INSTALL_ASTROPY: Dict[str, Dict[str, Any]] = {
    k: {
        "python": "3.9",
        "install": "pip install -e .[test]",
        "pre_install": ["pip install setuptools==68.0.0"],
        "pip_packages": [
            "attrs==23.1.0",
            "exceptiongroup==1.1.3",
            "execnet==2.0.2",
            "hypothesis==6.82.6",
            "iniconfig==2.0.0",
            "numpy==1.23.4",
            "packaging==23.1",
            "pluggy==1.3.0",
            "psutil==5.9.5",
            "pyerfa==2.0.0.3",
            "pytest-arraydiff==0.5.0",
            "pytest-astropy-header==0.2.2",
            "pytest-astropy==0.10.0",
            "pytest-cov==4.1.0",
            "pytest-doctestplus==1.0.0",
            "pytest-filter-subpackage==0.1.2",
            "pytest-mock==3.11.1",
            "pytest-openfiles==0.5.0",
            "pytest-remotedata==0.4.0",
            "pytest-xdist==3.3.1",
            "pytest==7.4.0",
            "PyYAML==6.0.1",
            "sortedcontainers==2.4.0",
            "tomli==2.0.1",
        ],
    }
    for k in ["0.1", "0.2", "0.3", "0.4", "1.1", "1.2", "1.3", "3.0", "3.1", "3.2"]
    + ["4.1", "4.2", "4.3", "5.0", "5.1", "5.2"]
}

for k in ["4.1", "4.2", "4.3", "5.0", "5.1", "5.2"]:
    MAP_VERSION_TO_INSTALL_ASTROPY[k]["pre_install"] = [
        'sed -i \'s/requires = \\["setuptools",/requires = \\["setuptools==68.0.0",/\' pyproject.toml'
    ]

MAP_VERSION_TO_INSTALL_SYMPY: Dict[str, Dict[str, Any]] = {
    k: {
        "python": "3.9",
        "packages": "mpmath flake8",
        "pip_packages": ["mpmath==1.3.0", "flake8-comprehensions"],
        "install": "pip install -e .",
    }
    for k in ["1.10", "1.11", "1.12", "1.2", "1.4", "1.5", "1.6"]
    + ["1.7", "1.8", "1.9"]
}

MAP_VERSION_TO_INSTALL_SYMPY.update(
    {
        k: {
            "python": "3.7",
            "packages": "mpmath flake8",
            "pip_packages": ["mpmath==1.3.0", "flake8-comprehensions"],
            "install": "pip install -e .",
        }
        for k in ["0.7", "1.0", "1.1"]
    }
)

MAP_VERSION_TO_INSTALL_SYMPY.update(
    {
        k: {
            "python": "3.9",
            "packages": "requirements.txt",
            "install": "pip install -e .",
            "pip_packages": ["mpmath==1.3.0"],
        }
        for k in ["1.13"]
    }
)

MAP_VERSION_TO_INSTALL_PYLINT: Dict[str, Dict[str, Any]] = {
    k: {
        "python": "3.9",
        "packages": "requirements.txt",
        "install": "pip install -e .",
        "pip_packages": ["pytest"],
    }
    for k in [
        "2.10",
        "2.11",
        "2.13",
        "2.14",
        "2.15",
        "2.16",
        "2.17",
        "2.8",
        "2.9",
        "3.0",
    ]
}

MAP_VERSION_TO_INSTALL_PYLINT["2.15"]["pre_test"] = ["pip install -e ."]

MAP_VERSION_TO_INSTALL_PYLINT.update(
    {
        k: {**MAP_VERSION_TO_INSTALL_PYLINT[k], "pip_packages": ["toml", "pytest"]}
        for k in ["2.13"]
    }
)

MAP_VERSION_TO_INSTALL_PYLINT.update(
    {
        k: {
            **MAP_VERSION_TO_INSTALL_PYLINT[k],
            "pip_packages": ["astroid==3.0.0a6", "pytest"],
        }
        for k in ["3.0"]
    }
)

MAP_VERSION_TO_INSTALL_XARRAY: Dict[str, Dict[str, Any]] = {
    k: {
        "python": "3.10",
        "packages": "environment.yml",
        "install": "pip install -e .",
        "pip_packages": [
            "numpy==1.25.2",
            "packaging==23.1",
            "pandas==1.5.3",
            "pytest==8.1.1",
            "python-dateutil==2.8.2",
            "pytz==2023.3",
            "six==1.16.0",
        ],
        "no_use_env": True,
    }
    for k in ["0.12", "0.18", "0.19", "0.20", "2022.03", "2022.06", "2022.09"]
}

MAP_VERSION_TO_INSTALL_SQLFLUFF: Dict[str, Dict[str, Any]] = {
    k: {
        "python": "3.9",
        "packages": "requirements.txt",
        "install": "pip install -e .",
    }
    for k in [
        "0.10",
        "0.11",
        "0.12",
        "0.13",
        "0.4",
        "0.6",
        "0.8",
        "0.9",
        "1.1",
        "1.2",
        "1.3",
        "1.4",
        "2.0",
        "2.1",
        "2.2",
    ]
}

MAP_VERSION_TO_INSTALL_PYVISTA: Dict[str, Dict[str, Any]] = {
    k: {
        "python": "3.9",
        "install": "pip install -e .",
        "pip_packages": ["pytest"],
    }
    for k in ["0.20", "0.21", "0.22", "0.23"]
}
MAP_VERSION_TO_INSTALL_PYVISTA.update(
    {
        k: {
            "python": "3.9",
            "packages": "requirements.txt",
            "install": "pip install -e .",
            "pip_packages": ["pytest"],
        }
        for k in [
            "0.24",
            "0.25",
            "0.26",
            "0.27",
            "0.28",
            "0.29",
            "0.30",
            "0.31",
            "0.32",
            "0.33",
            "0.34",
            "0.35",
            "0.36",
            "0.37",
            "0.38",
            "0.39",
            "0.40",
            "0.41",
            "0.42",
            "0.43",
        ]
    }
)

MAP_VERSION_TO_INSTALL_ASTROID: Dict[str, Dict[str, Any]] = {
    k: {
        "python": "3.9",
        "install": "pip install -e .",
        "pip_packages": ["pytest"],
    }
    for k in ["2.10", "2.12", "2.13", "2.14", "2.15", "2.5", "2.6", "2.7", "2.9", "3.0"]
}
for k in ["2.5", "2.6"]:
    MAP_VERSION_TO_INSTALL_ASTROID[k]["pip_packages"].extend(
        ["lazy_object_proxy==1.9.0", "wrapt==1.12.1"]
    )
for k in ["2.9", "2.10"]:
    MAP_VERSION_TO_INSTALL_ASTROID[k]["pip_packages"].extend(
        [
            "lazy_object_proxy==1.9.0",
            "wrapt==1.13.3",
            "typing-extensions==4.8.0",
            "setuptools==68.0.0",
        ]
    )
for k in ["2.12", "2.13", "2.14", "2.15"]:
    MAP_VERSION_TO_INSTALL_ASTROID[k]["pip_packages"].extend(
        ["lazy_object_proxy==1.9.0", "wrapt==1.15.0", "typing-extensions==4.8.0"]
    )
MAP_VERSION_TO_INSTALL_ASTROID["2.7"]["pip_packages"].extend(
    ["lazy_object_proxy==1.9.0", "wrapt==1.12.1", "typing-extensions==4.8.0"]
)
MAP_VERSION_TO_INSTALL_ASTROID["3.0"]["pip_packages"].append("typing-extensions==4.8.0")


MAP_VERSION_TO_INSTALL_MARSHMALLOW: Dict[str, Dict[str, Any]] = {
    k: {
        "python": "3.9",
        "install": "pip install -e '.[dev]'",
    }
    for k in ["2.18", "2.19", "2.20", "3.0", "3.12", "3.19", "3.9"]
}

MAP_VERSION_TO_INSTALL_PVLIB: Dict[str, Dict[str, Any]] = {
    k: {
        "python": "3.9",
        "install": "pip install -e .[all]",
        "packages": "pandas scipy",
        "pip_packages": ["jupyter", "ipython", "matplotlib", "pytest", "flake8"],
    }
    for k in ["0.5", "0.6", "0.7", "0.8", "0.9"]
}

MAP_VERSION_TO_INSTALL_PYDICOM: Dict[str, Dict[str, Any]] = {
    k: {
        "python": "3.6",
        "install": "pip install -e .",
        "packages": "numpy",
        "pip_packages": ["pytest"],
    }
    for k in ["1.2", "1.3", "1.4", "2.0", "2.1", "2.2", "2.3"]
}
MAP_VERSION_TO_INSTALL_PYDICOM.update(
    {
        k: {
            **MAP_VERSION_TO_INSTALL_PYDICOM[k],
            "python": "3.8",
            "pip_packages": ["pytest==4.6.11"],
        }
        for k in ["1.4", "2.0"]
    }
)
MAP_VERSION_TO_INSTALL_PYDICOM.update(
    {
        k: {
            **MAP_VERSION_TO_INSTALL_PYDICOM[k],
            "python": "3.9",
            "pip_packages": ["pytest==4.6.11"],
        }
        for k in ["2.1", "2.2"]
    }
)
MAP_VERSION_TO_INSTALL_PYDICOM.update(
    {k: {**MAP_VERSION_TO_INSTALL_PYDICOM[k], "python": "3.10"} for k in ["2.3"]}
)

MAP_VERSION_TO_INSTALL_HUMANEVAL: Dict[str, Dict[str, str]] = {
    k: {"python": "3.9"} for k in ["1.0"]
}

# Constants - Task Instance Installation Environment
MAP_VERSION_TO_INSTALL: Dict[str, Dict[str, Dict[str, Any]]] = {
    "astropy/astropy": MAP_VERSION_TO_INSTALL_ASTROPY,
    "django/django": MAP_VERSION_TO_INSTALL_DJANGO,
    "matplotlib/matplotlib": MAP_VERSION_TO_INSTALL_MATPLOTLIB,
    "marshmallow-code/marshmallow": MAP_VERSION_TO_INSTALL_MARSHMALLOW,
    "mwaskom/seaborn": MAP_VERSION_TO_INSTALL_SEABORN,
    "pallets/flask": MAP_VERSION_TO_INSTALL_FLASK,
    "psf/requests": MAP_VERSION_TO_INSTALL_REQUESTS,
    "pvlib/pvlib-python": MAP_VERSION_TO_INSTALL_PVLIB,
    "pydata/xarray": MAP_VERSION_TO_INSTALL_XARRAY,
    "pydicom/pydicom": MAP_VERSION_TO_INSTALL_PYDICOM,
    "pylint-dev/astroid": MAP_VERSION_TO_INSTALL_ASTROID,
    "pylint-dev/pylint": MAP_VERSION_TO_INSTALL_PYLINT,
    "pytest-dev/pytest": MAP_VERSION_TO_INSTALL_PYTEST,
    "pyvista/pyvista": MAP_VERSION_TO_INSTALL_PYVISTA,
    "scikit-learn/scikit-learn": MAP_VERSION_TO_INSTALL_SKLEARN,
    "sphinx-doc/sphinx": MAP_VERSION_TO_INSTALL_SPHINX,
    "sqlfluff/sqlfluff": MAP_VERSION_TO_INSTALL_SQLFLUFF,
    "swe-bench/humaneval": MAP_VERSION_TO_INSTALL_HUMANEVAL,
    "sympy/sympy": MAP_VERSION_TO_INSTALL_SYMPY,
}

# Constants - Repository Specific Installation Instructions
MAP_REPO_TO_INSTALL: Dict[str, Any] = {}

# Constants - Task Instance Test Frameworks
TEST_PYTEST: str = "coverage run -m pytest --no-header -rA --tb=no -p no:cacheprovider"
TEST_PYTEST_SKIP_NO_HEADER: str = (
    "coverage run -m pytest -rA --tb=no -p no:cacheprovider"
)
MAP_REPO_TO_TEST_FRAMEWORK: Dict[str, str] = {
    "astropy/astropy": TEST_PYTEST,
    "django/django": "coverage run ./tests/runtests.py --verbosity 2",
    "marshmallow-code/marshmallow": TEST_PYTEST,
    "matplotlib/matplotlib": TEST_PYTEST,
    "mwaskom/seaborn": "coverage run -m pytest --no-header -rA",
    "pallets/flask": TEST_PYTEST,
    "psf/requests": TEST_PYTEST,
    "pvlib/pvlib-python": TEST_PYTEST,
    "pydata/xarray": TEST_PYTEST,
    "pydicom/pydicom": TEST_PYTEST_SKIP_NO_HEADER,
    "pylint-dev/astroid": TEST_PYTEST,
    "pylint-dev/pylint": TEST_PYTEST,
    "pytest-dev/pytest": "coverage run -m pytest -rA",
    "pyvista/pyvista": TEST_PYTEST,
    "scikit-learn/scikit-learn": TEST_PYTEST_SKIP_NO_HEADER,
    "sphinx-doc/sphinx": "tox -epy39 -v --",
    "sqlfluff/sqlfluff": TEST_PYTEST,
    "swe-bench/humaneval": "coverage run python",
    "sympy/sympy": "coverage run bin/test --no-subprocess -C --verbose",
}

# Constants - Task Instance Requirements File Paths
MAP_REPO_TO_REQS_PATHS: Dict[str, List[str]] = {
    "django/django": ["tests/requirements/py3.txt"],
    "matplotlib/matplotlib": [
        "requirements/dev/dev-requirements.txt",
        "requirements/testing/travis_all.txt",
    ],
    "pallets/flask": ["requirements/dev.txt"],
    "pylint-dev/pylint": ["requirements_test.txt"],
    "pyvista/pyvista": ["requirements_test.txt", "requirements.txt"],
    "sqlfluff/sqlfluff": ["requirements_dev.txt"],
    "sympy/sympy": ["requirements-dev.txt"],
}

# Constants - Task Instance environment.yml File Paths
MAP_REPO_TO_ENV_YML_PATHS: Dict[str, List[str]] = {
    "matplotlib/matplotlib": ["environment.yml"],
    "pydata/xarray": ["ci/requirements/environment.yml", "environment.yml"],
}

MAP_REPO_TO_DEB_PACKAGES: Dict[str, List[str]] = {
    "matplotlib/matplotlib": [
        "texlive",
        "texlive-xetex",
        "dvipng",
        "ghostscript",
        "libfreetype-dev",
        "libtiff-dev",
    ],
    "pyvista/pyvista": ["libgl1", "libxrender1"],
}

# Constants - Evaluation Keys
KEY_INSTANCE_ID: str = "instance_id"
KEY_ID: str = "id"
KEY_MODEL: str = "model_name_or_path"
KEY_PREDICTIONS: str = "preds"
KEY_TEST_FILE_PATH: str = "test_file"
KEY_BASELINES: str = "preds_context"

# Constants - Logging
APPLY_PATCH_FAIL: str = ">>>>> Patch Apply Failed"
APPLY_PATCH_PASS: str = ">>>>> Applied Patch"
INSTALL_FAIL: str = ">>>>> Init Failed"
INSTALL_PASS: str = ">>>>> Init Succeeded"
INSTALL_TIMEOUT: str = ">>>>> Init Timed Out"
RESET_FAILED: str = ">>>>> Reset Failed"
TESTS_ERROR: str = ">>>>> Tests Errored"
TESTS_FAILED: str = ">>>>> Some Tests Failed"
UNFILTERED_TESTS_FAILED: str = ">>>>> Unfiltered Tests Failed"
TESTS_CONFIG: str = ">>>>> Tests config"
TESTS_PASSED: str = ">>>>> All Tests Passed"
UNFILTERED_TESTS_PASSED: str = ">>>>> Unfiltered Tests Passed"
TESTS_TIMEOUT: str = ">>>>> Tests Timed Out"

SETTING_PROMPT_MAP: Dict[str, str] = {
    "none": "none",
    "first": "preamble",
    "last": "last_minus_one",
    "extra": "last",
}
VALID_K: List[int] = [0, 1, 5, 10, 100]


# Constants - Patch Types
class PatchType(Enum):
    PATCH_GOLD = "gold"
    PATCH_PRED = "pred"
    PATCH_PRED_TRY = "pred_try"
    PATCH_PRED_MINIMAL = "pred_minimal"
    PATCH_PRED_MINIMAL_TRY = "pred_minimal_try"
    PATCH_TEST = "test"

    def __str__(self) -> str:
        return self.value


# Constants - Miscellaneous
NON_TEST_EXTS: List[str] = [
    ".json",
    ".png",
    "csv",
    ".txt",
    ".md",
    ".jpg",
    ".jpeg",
    ".pkl",
    ".yml",
    ".yaml",
    ".toml",
]
SWE_BENCH_URL_RAW: str = "https://raw.githubusercontent.com/"


MUTATION_TEMPLATE: str = """[cosmic-ray]
module-path = "{source_fp}"
timeout = {timeout}
excluded-modules = []
test-command = "{test_cmd}"

[cosmic-ray.distributor]
name = "local"
"""
