# -*- coding: utf-8 -*-

from __future__ import with_statement
from setuptools import setup


version = '1.1.4'


setup(
    name='TimeConvert',
    version=version,
    keywords='',
    description="Time Convert for Humans",
    long_description=open('README.rst').read(),

    url='https://github.com/Brightcells/TimeConvert',

    author='Hackathon',
    author_email='kimi.huang@brightcells.com',

    py_modules=['TimeConvert'],
    install_requires=['pytz', ],

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
