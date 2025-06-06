from setuptools import setup, find_packages

setup(
    name = "PyShift",
    packages = find_packages(),
    version = "1.1.1",
    description = "Work schedule library for Python",
    author = "Kent Randall",
    author_email = "point85.llc@gmail.com",
    url="https://github.com/point85/PyShift",
    keywords = ["shift", "work schedule", "shift calendar", "Python"],
    classifiers = [
        "Programming Language :: Python :: 3",
        "Development Status :: Released",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Work Schedule :: Shift work calendar",
        ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.9',
)

