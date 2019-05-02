"""Setup for rio-tiler-glob."""

from setuptools import setup, find_packages

with open("rio_tiler_glob/__init__.py") as f:
    for line in f:
        if line.find("__version__") >= 0:
            version = line.split("=")[1].strip()
            version = version.strip('"')
            version = version.strip("'")
            continue

# Runtime requirements.
inst_reqs = ["rio-tiler",  "lambda-proxy~=3.0.0", "rio-color", "braceexpand"]
extra_reqs = {}

setup(
    name="rio-tiler-glob",
    version=version,
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
)
