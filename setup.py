# -*- coding: utf-8 -*-
"""
pycri-spotify
-------------

Plugin for fetching data from spotify.
"""
from setuptools import setup

setup(
    name='pycri-spotify',
    version='0.2.0',
    description='Spotify plugin for pycri',
    long_description=__doc__,
    author='Marcus Carlsson',
    author_email='carlsson.marcus@gmail.com',
    url='https://github.com/xintron/pycri-spotify',
    packages=['pycri_spotify'],
    provides='pycri_spotify',
    install_requires=['pycri'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Framework :: Twisted',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Topic :: Communications :: Chat :: Internet Relay Chat',
    ]
)
