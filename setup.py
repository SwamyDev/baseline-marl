from pathlib import Path

from setuptools import find_packages, setup

here = Path(__file__).absolute().parent

long_description = (here / Path('README.md')).read_text()

_version = {}
exec((here / Path('baseline-marl/_version.py')).read_text(), _version)

setup(
    name='baseline-marl',
    version=_version['__version__'],
    description='Extend baseline3 package to be used with multi-agent environmnets',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SwamyDev/baseline-marl',
    author='Bernhard Raml',
    packages=find_packages(include=['baseline-marl', 'baseline-marl.*']),
    extras_require={"test": ['pytest', 'pytest-cov', 'gym-quickcheck']},
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.6',
)
