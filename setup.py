from setuptools import setup, find_packages

setup(
    name="manmandon",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "selenium-wire",
	    "click",
        "toml"
    ],
    entry_points={
        "console_scripts": [
            "mmdon = manmandon.main:main"
        ]
    },
    package_data={
        "": "default.toml"
    }
)
