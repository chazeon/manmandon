from setuptools import setup, find_packages

setup(
    name="manmandon",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "playwright",
	    "click",
        "toml",
        "deepmerge",
        "urlmatch",
        "tqdm",
        "requests",
    ],
    extras_require={
        'dev': [
            'pdoc',
            'mypy',
            'types-toml',
            'tqdm-stubs',
            # 'pytest',
            # 'pytest-cov',
        ]
    },
    entry_points={
        "console_scripts": [
            "mmdon = manmandon.main:main",
        ]
    },
    package_data={
        "": ["default.toml"],
    }
)
