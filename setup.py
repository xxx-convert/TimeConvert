# -*- coding: utf-8 -*-

from setuptools import setup


version = '1.3.16'


setup(
    name='TimeConvert',
    version=version,
    keywords='',
    description='Time Convert for Humans™',
    long_description=open('README.rst').read(),

    url='https://github.com/xxx-convert/TimeConvert',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    packages=['TimeConvert'],
    py_modules=[],
    install_requires=['pytz', 'tzlocal'],

    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
