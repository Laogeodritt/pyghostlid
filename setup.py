import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='PyGhostLid',
    version='0.2.0',
    packages=['ghostlid'],
    license='Modified BSD',
    author='Marc-Alexandre Chan',
    author_email='laogeodritt@arenthil.net',
    url='https://github.com/Laogeodritt/pyghostlid',
    download_url='https://github.com/Laogeodritt/pyghostlid/tarball/0.2.0',
    keywords=['ghostbin', 'pastebin', 'api', 'upload'],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: BSD License',
                 'Topic :: Software Development :: Libraries :: Python Modules'],
    setup_requires=[],
    zip_safe=True,
    description='Submit and retrieve pastes from GhostBin within your application! '
                'Supports both ghostbin.com and any self-hosted instances of ghostbin.',
    long_description=read('README.rst')
)
