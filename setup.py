from setuptools import setup, find_namespace_packages

setup(
    name='ceaos_networkactuation',
    version='0.0.1',
    packages=find_namespace_packages(include=['ceaos.*']),
    install_requires=[
        'pyzmq'
    ]
)