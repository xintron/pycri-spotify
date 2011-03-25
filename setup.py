# -*- coding: utf-8 -*-
from setuptools import setup

from spotify import __version__

setup(
    name='pycri-spotify',
    version=__version__,
    description='Spotify plugin for pycri',
    long_description=open('README.md').read(),
    author='Marcus Carlsson',
    author_email='carlsson.marcus@gmail.com',
    url='https://github.com/xintron/pycri-spotify',
    packages=['spotify'],
    provides=[
        'pycri_spotify',
    ],
    install_requires=['pycri>=0.3'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Framework :: Twisted',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
    ]
)
