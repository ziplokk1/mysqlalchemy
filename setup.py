from __future__ import unicode_literals

from setuptools import setup

VERSION = '1.0.0'

REQUIREMENTS = [
    'mysqlclient==1.3.9',
    'SQLAlchemy==1.1.11',
]

setup(
    name='incapsula-cracker-py3',
    version=VERSION,
    packages=['mysqlalchemy'],
    url='https://github.com/ziplokk1/incapsula-cracker-py3',
    license='LICENSE.txt',
    author='Mark Sanders',
    author_email='sdscdeveloper@gmail.com',
    install_requires=REQUIREMENTS,
    description='A way to bypass incapsula robot checks when using requests.',
    include_package_data=True
)
