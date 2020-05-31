import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="poddl",
    version="0.3.0",
    description="Downloads podcasts from RSS feeds",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/benkyriakou/poddl",
    author="Ben Kyriakou",
    author_email="benkyriakou@users.noreply.github.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
    ],
    packages=["poddl"],
    include_package_data=True,
    install_requires=["requests", "unidecode"],
    entry_points={
        "console_scripts": [
            "poddl=poddl.util:main",
        ]
    },
)
