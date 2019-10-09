from distutils.core import setup

setup(
    name = "PyShift",
    packages = ["PyShift"],
    version = "1.0.0",
    description = "Work schedule library for Python",
    author = "Kent Randall",
    author_email = "point85.llc@gmail.com",
    # url = "http://chardet.feedparser.org/",
    # download_url = "http://chardet.feedparser.org/download/python3-chardet-1.0.1.tgz",
    keywords = ["shift", "work schedule", "shift calendar", "Python"],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: Released",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Work Schedule :: Shift work calendar",
        ],
    long_description = 
	"""
    The PyShift library manages work schedules.  A work schedule consists of one or more teams who rotate through a sequence of shift and off-shift periods of time.  The PyShift project allows breaks during shifts to be defined as well as non-working periods of time (e.g. holidays and scheduled maintenance periods) that are applicable to the entire work schedule.
	"""
)