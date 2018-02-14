
try:
    import sage.all
except ImportError:
    raise ValueError("this package should be installed inside Sage")

from distutils.core import setup

setup(
    name = "ore_algebra",
    version = "0.3",
    author = "Manuel Kauers, Maximilian Jaroschek, Fredrik Johansson",
    author_email = "manuel@kauers.de",
    licence = "GPL",
    packages = ["ore_algebra", "ore_algebra.analytic"]
    )
    
