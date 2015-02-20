from setuptools import setup

import mailip


setup(
    name = "mailip",
    version = mailip.__version__,
    description="Program that send you an email when your IP changes",
    packages=['mailip',],
    license='GNU',
    long_description=open('README.txt').read(),
    entry_points={
        'console_scripts' : [
            'mailip=mailip:main'
        ],
    },
)
