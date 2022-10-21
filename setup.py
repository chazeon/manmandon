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
        "coloredlogs",
        "tabulate",
        "wcwidth", # https://stackoverflow.com/a/66648740/1487532
    ],
    extras_require={
        'dev': [
            'pdoc',
            'mypy',
            'types-toml',
            'types-tqdm',
            'types-tabulate'
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
        "manmandon": ["default.toml"],
    },
    license="MIT"
)
