from __future__ import unicode_literals

from setuptools import setup

VERSION = '1.0.0'

REQUIREMENTS = [
    'mysqlclient==1.3.9',
    'SQLAlchemy==1.1.11',
]

setup(
    name='mysqlalchemy',
    version=VERSION,
    packages=['mysqlalchemy'],
    url='https://github.com/ziplokk1/mysqlalchemy',
    license='LICENSE.txt',
    author='Mark Sanders',
    author_email='sdscdeveloper@gmail.com',
    install_requires=REQUIREMENTS,
    description='MySQL wrapper for sqlalchemy.',
    include_package_data=True
)
