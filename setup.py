from setuptools import setup

setup(
    name='abc2db',
    version='1.0.2',
    packages=['abc2db'],
    url='',
    license='',
    author='Phoenix',
    author_email='vova24848@gmail.com',
    description='Convert abstract repositories to db classes',
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    install_requires=[
        'pydantic>=1.10.4',
    ]
)
