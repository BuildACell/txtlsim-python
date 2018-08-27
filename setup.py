# setup.py - setup script for TX-TL modeling toolbox
# RMM, 26 Aug 2018

from setuptools import setup

# Get the long description from the README file
with open('README.md') as fp:
    long_description = fp.read()

setup(
    name = 'txtl',
    version = '0.1',
    author = 'BuildACell',
    author_email = 'murray@cds.caltech.edu',
    url = 'https://github.com/BuildACell/txtlsim-python',
    description = 'TX-TL simulation toolbox in Python',
    long_description = long_description,
    packages = ['txtl', 'tests'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development',
        'Topic :: Scientific/Engineering',
        'Operating System :: POSIX',
        'Operating System :: Unix'
        'Operating System :: MacOS'
    ],
    test_suite = 'nose.collector',
)
